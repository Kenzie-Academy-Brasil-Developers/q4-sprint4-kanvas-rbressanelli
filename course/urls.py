from django.urls import path

from .views import CourseView

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<course_id>/", CourseView.as_view()),
    path("courses/<course_id>/registrations/instructor/", CourseView.as_view()),
    path("courses/<course_id>/registrations/students/", CourseView.as_view()),
]
