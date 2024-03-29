from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status

from ongs.models import Ong
from ongs.permissions import IsOngOwner
from ongs.views import OngGenericView
from sos_brazil.exceptions import (
    IncorrectUUIDException,
    MissingKeyException,
    NotFoundException,
    WrongValueException,
)
from sos_brazil.settings import DATE_INPUT_FORMATS

from .models import Campaign
from .serializers import CampaignSerializer, DonationSerializer


class CampaignGenericView(APIView):
    def get_campaign_or_404(self, campaign_id: str):
        try:
            campaign = get_object_or_404(Campaign, pk=campaign_id)
            return campaign
        except Http404:
            raise NotFoundException("campaign")
        except ValidationError:
            raise IncorrectUUIDException


class OngCampaignView(OngGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOngOwner]

    def post(self, request: Request, ong_id: str):
        ong = self.get_ong_or_404(ong_id)
        self.check_object_permissions(request, ong)

        serialized = CampaignSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(ong=ong)

        return Response(serialized.data, status.HTTP_201_CREATED)

    def get(self, _: Request, ong_id: str):
        self.get_ong_or_404(ong_id)

        campaigns = Campaign.objects.filter(ong_id=ong_id)
        serialized = CampaignSerializer(instance=campaigns, many=True)

        return Response({"ong_campaigns": serialized.data}, status.HTTP_200_OK)


class CampaignView(APIView):
    def get(self, _: Request):
        campaigns = Campaign.objects.all()

        serialized = CampaignSerializer(instance=campaigns, many=True)

        return Response({"campaigns": serialized.data}, status.HTTP_200_OK)


class CampaignIdView(CampaignGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOngOwner]

    def get(self, _: Request, campaign_id: str):
        campaign = self.get_campaign_or_404(campaign_id)

        serialized = CampaignSerializer(campaign)

        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, request: Request, campaign_id: str):
        campaign = self.get_campaign_or_404(campaign_id)
        self.check_object_permissions(request, campaign.ong)

        if campaign.collected > 0:
            return Response(
                {
                    "error": "Cannot delete an campaign that has collected value higher than zero"
                },
                status.HTTP_403_FORBIDDEN,
            )

        campaign.delete()

        return Response("", status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, campaign_id: str):
        campaign = self.get_campaign_or_404(campaign_id)
        self.check_object_permissions(request, campaign.ong)

        try:
            serialized = CampaignSerializer(
                instance=campaign, data=request.data, partial=True
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()
        except KeyError as err:
            return Response({"error": err.args[0]}, status.HTTP_400_BAD_REQUEST)

        return Response(serialized.data, status.HTTP_200_OK)


class DonationView(CampaignGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, campaign_id: str):
        campaign = self.get_campaign_or_404(campaign_id)

        data = request.data
        user = request.user

        if not "value" in data:
            raise MissingKeyException("value", "The value must be informed.")

        value = data["value"]

        if value <= 0:
            raise WrongValueException("The value must be positive.")

        updated_campaign = {
            **campaign.__dict__,
            "collected": campaign.collected + value,
        }

        if updated_campaign["collected"] >= campaign.goal:
            updated_campaign["goal_reached"] = True

        serialized = CampaignSerializer(
            instance=campaign, data=updated_campaign, context="donation"
        )
        serialized.is_valid(raise_exception=True)
        serialized.save()

        donation = DonationSerializer(data=data)
        donation.is_valid(raise_exception=True)
        donation.save(user=user, campaign=campaign)

        return Response(donation.data, status.HTTP_201_CREATED)


class CampaignEndView(CampaignGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOngOwner]

    def post(self, request: Request, campaign_id: str):
        campaign = self.get_campaign_or_404(campaign_id)
        self.check_object_permissions(request, campaign.ong)

        time_now = timezone.now().strftime(DATE_INPUT_FORMATS[0])

        updated_campaign = {
            **campaign.__dict__,
            "is_active": False,
            "end_date": time_now,
        }

        serialized = CampaignSerializer(
            instance=campaign, data=updated_campaign, context="end_campaign"
        )

        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status.HTTP_200_OK)
