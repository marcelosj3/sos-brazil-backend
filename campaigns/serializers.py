from ongs.serializers import OngSerializer
from rest_framework import serializers

from .models import Campaign, Donation


class CampaignSerializer(serializers.Serializer):
    campaign_id = serializers.UUIDField(read_only=True)

    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255)
    collected = serializers.FloatField(required=False)
    goal = serializers.FloatField()
    goal_reached = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    ong_id = OngSerializer(read_only=True)

    def create(self, validated_data: dict):
        campaign = Campaign.objects.create(**validated_data)

        return campaign


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = "__all__"

    def create(self, validated_data: dict):
        donation = Donation.objects.create(**validated_data)

        return donation
