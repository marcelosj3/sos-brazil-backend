from django.urls import path

from .views import UserIdPasswordView, UserLoginView, UserView

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<str:user_id>/password/", UserIdPasswordView.as_view()),
    path("users/login/", UserLoginView.as_view()),
]
