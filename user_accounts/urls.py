from django.urls import path

from .views import KanvasUserLoginView, KanvasUserView

urlpatterns = [
    path("accounts/", KanvasUserView.as_view()),
    path("login/", KanvasUserLoginView.as_view()),
]
