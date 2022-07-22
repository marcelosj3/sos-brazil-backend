from django.urls import path

from .views import OngView

urlpatterns = [path("ongs/", OngView.as_view())]
