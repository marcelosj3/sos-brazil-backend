from django.urls import path

from .views import OngIdView, OngView

urlpatterns = [
    path("ongs/", OngView.as_view()),
    path("ongs/<int:ong_id>/", OngIdView.as_view()),
]
