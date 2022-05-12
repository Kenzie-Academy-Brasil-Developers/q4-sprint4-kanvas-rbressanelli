from rest_framework import serializers

from user_accounts.serializers import KanvasUserSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    created_at = serializers.DateTimeField(read_only=True)
    link_repo = serializers.CharField()
    instructor = KanvasUserSerializer(read_only=True)
    students = KanvasUserSerializer(many=True, read_only=True)


class CourseUUIDSerializer(serializers.Serializer):
    course_id = serializers.UUIDField()


class CoursePatchSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    demo_time = serializers.TimeField(required=False)
    link_repo = serializers.CharField(required=False)


class CourseInstructorUUIDSerializer(serializers.Serializer):
    instructor_id = serializers.UUIDField()


class CourseStudentUUIDSerializer(serializers.Serializer):
    students_id = serializers.UUIDField()
