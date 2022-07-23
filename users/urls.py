from django.urls import path

from .views import UserLoginView, UserView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/login/", UserLoginView.as_view()),
]
