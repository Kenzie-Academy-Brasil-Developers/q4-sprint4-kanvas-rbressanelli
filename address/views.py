from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from address.models import Address
from user_accounts.models import KanvasUser

from .serializers import AddressSerializer


class AddressView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):

        user = KanvasUser.objects.filter(email=request.user).all()

        serializer = AddressSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        found_user = Address.objects.filter(users=user[0])
        if found_user:
            serializer = AddressSerializer(found_user[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        verify_address = Address.objects.filter(zip_code=request.data["zip_code"])

        if len(verify_address) > 0:
            user.update(address=verify_address[0])
            serializer = AddressSerializer(verify_address[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        new_address = Address.objects.create(**serializer.validated_data)
        user.update(address=new_address)

        address = Address.objects.filter(pk=new_address.uuid)

        serializer = AddressSerializer(address[0])

        return Response(serializer.data, status=status.HTTP_200_OK)
