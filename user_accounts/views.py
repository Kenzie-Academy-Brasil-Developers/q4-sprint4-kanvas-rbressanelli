from urllib import request
from wsgiref.util import request_uri

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user_accounts.permissions import Authenticated

from .models import KanvasUser
from .serializers import KanvasUserLoginSerializer, KanvasUserSerializer

# Create your views here.


class KanvasUserView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [Authenticated]

    def post(self, request):

        serializer = KanvasUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        find_user = KanvasUser.objects.filter(
            email=serializer.validated_data["email"]
        ).exists()

        if find_user == True:
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = KanvasUser.objects.create_user(**serializer.validated_data)

        serializer = KanvasUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        verify_permition = get_object_or_404(KanvasUser, email=request.user)

        if not verify_permition.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        users = KanvasUser.objects.all()

        serializer = KanvasUserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class KanvasUserLoginView(APIView):
    def post(self, request):
        serializer = KanvasUserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({"token": token.key})

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
