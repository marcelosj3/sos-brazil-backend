from django.urls import path

from .views import CampaignIdView, CampaignView, DonationView, OngCampaignView

urlpatterns = [
    path("ongs/<str:ong_id>/campaigns/", OngCampaignView.as_view()),
    path("campaigns/", CampaignView.as_view()),
    path("campaigns/<str:campaign_id>/", CampaignIdView.as_view()),
    path("campaigns/<str:campaign_id>/donate/", DonationView.as_view()),
]
