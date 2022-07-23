from django.urls import path

from .views import OngIdView, OngView

urlpatterns = [
    path("ongs/", OngView.as_view()),
    path("ongs/<str:ong_id>/", OngIdView.as_view()),
]
