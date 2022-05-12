from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from course.permissions import Authenticated
from user_accounts.models import KanvasUser

from .serializers import (CourseInstructorUUIDSerializer,
                          CoursePatchSerializer, CourseSerializer,
                          CourseStudentUUIDSerializer, CourseUUIDSerializer)


class CourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [Authenticated]

    def post(self, request):

        user = KanvasUser.objects.filter(email=request.user).all()[0]

        if not user.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            request.data["students"] = []

            serializer = CourseSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            course = Course.objects.create(**serializer.validated_data, instructor=None)

            serializer = CourseSerializer(course)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as err:
            return Response(
                {"message": "Course already exists"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def get(self, request, course_id=None):

        try:
            if course_id:
                serializer = CourseUUIDSerializer(data={"course_id": course_id})
                if not serializer.is_valid():
                    return Response(
                        {"message": "URL parameter must be a valid UUID"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                course = get_object_or_404(Course, pk=course_id)
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)

            courses = Course.objects.all()

            serializer = CourseSerializer(courses, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Http404:
            return Response(
                {"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, course_id):

        serializer = CourseUUIDSerializer(data={"course_id": course_id})
        if not serializer.is_valid():
            return Response(
                {"message": "URL parameter must be a valid UUID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verify_permition = get_object_or_404(KanvasUser, email=request.user)
        if not verify_permition.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:

            serializer = CoursePatchSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            name_already_exists = Course.objects.filter(name=request.data["name"])
            if name_already_exists:
                return Response(
                    {"message": "This course name already exists"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )
            course = Course.objects.filter(pk=course_id)
            course.update(**serializer.validated_data)
            serializer = CourseSerializer(course[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        except (Http404, IndexError):
            return Response(
                {"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
            )       

    def put(self, request, course_id):
        serializer = CourseUUIDSerializer(data={"course_id": course_id})
        if not serializer.is_valid():
            return Response(
                {"message": "URL parameter must be a valid UUID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        verify_permition = get_object_or_404(KanvasUser, email=request.user)
        if not verify_permition.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            user_type = [user for user in request.data.keys()]
            if user_type[0] == "instructor_id":
                serializer = CourseInstructorUUIDSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instructor = get_object_or_404(
                    KanvasUser, pk=request.data["instructor_id"]
                )

                if not instructor.is_admin:
                    return Response(
                        {"message": "Instructor id does not belong to an admin"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )

                course = Course.objects.filter(instructor=instructor)

                course.update(instructor=None)

                course = Course.objects.filter(pk=course_id)

                if len(course) == 0:
                    return Response(
                        {"message": "Course does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                course = Course.objects.filter(pk=course_id)
                course.update(instructor=instructor)
                serializer = CourseSerializer(course[0])

                return Response(serializer.data)

            elif user_type[0] == "students_id":
                students_serializer = []
                for user_uuid in request.data["students_id"]:
                    serializer = CourseStudentUUIDSerializer(
                        data={"students_id": user_uuid}
                    )
                    serializer.is_valid(raise_exception=True)
                    students_serializer.append(serializer)

                course = Course.objects.filter(pk=course_id)

                if len(course) == 0:
                    return Response(
                        {"message": "Course does not exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                for student in students_serializer:
                    students = get_object_or_404(
                        KanvasUser, pk=student.data["students_id"]
                    )
                    if students.is_admin:
                        return Response(
                            {"message": "Some student id belongs to an Instructor"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        )

                    course[0].students.add(students)
                serializer = CourseSerializer(course[0])
                return Response(serializer.data)

            else:
                user_type = request.get_full_path().split("/")[-2]
                return Response({f"{user_type}_id"}, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            if user_type[0] == "instructor_id":
                output_response = "Invalid instructor_id"
            else:
                output_response = "Invalid students_id list"
            return Response(
                {"message": f"{output_response}"}, status=status.HTTP_404_NOT_FOUND
            )        

    def delete(self, request, course_id):
        serializer = CourseUUIDSerializer(data={"course_id": course_id})
        if not serializer.is_valid():
            return Response(
                {"message": "URL parameter must be a valid UUID"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        verify_permition = get_object_or_404(KanvasUser, email=request.user)
        if not verify_permition.is_admin:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            course = get_object_or_404(Course, pk=course_id)
            serializer = CourseSerializer(course)

            course.delete()

            return Response("", status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response(
                {"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND
            )
