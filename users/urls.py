from django.urls import path

from .views import UserIdView, UserLoginView, UserView

urlpatterns = [
    path("users/login/", UserLoginView.as_view()),
    path("users/", UserView.as_view()),
    path("users/<str:user_id>/", UserIdView.as_view()),
]
