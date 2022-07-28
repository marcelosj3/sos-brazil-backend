from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from ongs.models import Ong
from ongs.permissions import isOngOwner
from sos_brazil.settings import DATE_INPUT_FORMATS

from .models import Campaign
from .permissions import CampaignPermission
from .serializers import CampaignSerializer, DonationSerializer


class OngCampaignView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CampaignPermission]

    def post(self, request: Request, ong_id: str):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)

            serialized = CampaignSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save(ong=ong)

            return Response(serialized.data, status.HTTP_201_CREATED)

        except Http404:
            return Response({"details": "Ong not found."}, status.HTTP_404_NOT_FOUND)

    def get(self, _: Request, ong_id: str):
        campaigns = Campaign.objects.filter(ong_id=ong_id)
        serialized = CampaignSerializer(instance=campaigns, many=True)

        return Response({"ong_campaigns": serialized.data}, status.HTTP_200_OK)


class CampaignView(APIView):
    def get(self, _: Request):
        campaigns = Campaign.objects.all()

        serialized = CampaignSerializer(instance=campaigns, many=True)

        return Response({"campaigns": serialized.data}, status.HTTP_200_OK)


class CampaignIdView(APIView):
    def get(self, _: Request, campaign_id: str):
        try:
            campaign = get_object_or_404(Campaign, pk=campaign_id)

            serialized = CampaignSerializer(campaign)

            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response(
                {"details": "Campaign not found."}, status.HTTP_404_NOT_FOUND
            )

    def delete(self, response: Response, campaign_id: str):
        try:
            find_campaign = get_object_or_404(Campaign, pk=campaign_id)

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        if find_campaign.collected > 0:
            return Response(
                {"error": "Collected field has to be '0' to be deleted"},
                status.HTTP_403_FORBIDDEN,
            )

        find_campaign.delete()

        return Response("", status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, campaign_id: str):
        try:
            campaign = get_object_or_404(Campaign, pk=campaign_id)

            serialized = CampaignSerializer(
                instance=campaign, data=request.data, partial=True
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(serialized.data, status.HTTP_200_OK)

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except KeyError as err:
            return Response({"error": err.args[0]}, status.HTTP_400_BAD_REQUEST)


class DonationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CampaignPermission]

    def post(self, request: Request, ong_id: str, campaign_id: str):
        try:
            get_object_or_404(Ong, pk=ong_id)
            campaign = get_object_or_404(Campaign, pk=campaign_id)

            data = request.data
            user = request.user

            if not "value" in data:
                return Response(
                    {"details": "The value must be informed."},
                    status.HTTP_400_BAD_REQUEST,
                )

            value = data["value"]

            if value <= 0:
                return Response(
                    {"details": "The value must be positive."},
                    status.HTTP_400_BAD_REQUEST,
                )

            donation = DonationSerializer(data=data)
            donation.is_valid(raise_exception=True)
            donation.save(user=user, campaign=campaign)

            updated_campaign = {
                **campaign.__dict__,
                "collected": campaign.collected + value,
            }

            if updated_campaign["collected"] >= campaign.goal:
                updated_campaign["goal_reached"] = True

            serialized = CampaignSerializer(
                instance=campaign,
                data=updated_campaign,
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()

            return Response(donation.data, status.HTTP_201_CREATED)

        except Http404:
            return Response(
                {"details": "Campaign not found."}, status.HTTP_404_NOT_FOUND
            )


class CampaignEndView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isOngOwner]

    def post(self, request: Request, campaign_id: str):
        try:
            campaign = get_object_or_404(Campaign, pk=campaign_id)
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

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Http404:
            return Response(
                {"details": "Campaign not found."}, status.HTTP_404_NOT_FOUND
            )
