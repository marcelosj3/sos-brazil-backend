from django.urls import path

from .views import OngIdRegisterAdmin, OngIdView, OngView

urlpatterns = [
    path("ongs/", OngView.as_view()),
    path("ongs/<str:ong_id>/", OngIdView.as_view()),
    path("ongs/<str:ong_id>/register_admin/", OngIdRegisterAdmin.as_view()),
]
