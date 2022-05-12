import uuid

from django.db import models

from user_accounts.models import KanvasUser


class Course(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    link_repo = models.CharField(max_length=255)
    instructor = models.OneToOneField(KanvasUser, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(KanvasUser, related_name="courses")
