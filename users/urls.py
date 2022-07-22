from django.urls import path

from .views import UserLoginView

urlpatterns = [
    path("users/login/", UserLoginView.as_view()),
]
