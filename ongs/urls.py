from django.urls import path

from .views import OngIdManageAdmins, OngIdView, OngView

urlpatterns = [
    path("ongs/", OngView.as_view()),
    path("ongs/<str:ong_id>/", OngIdView.as_view()),
    path("ongs/<str:ong_id>/admins/", OngIdManageAdmins.as_view()),
]
