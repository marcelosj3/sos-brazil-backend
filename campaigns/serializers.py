from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Campaign, Donation


class CampaignSerializer(serializers.Serializer):
    ong_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source="ong",
    )
    campaign_id = serializers.UUIDField(read_only=True)

    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=255)
    collected = serializers.FloatField(required=False)
    goal = serializers.FloatField()
    goal_reached = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate_goal(self, value):
        if(value <= 0):
            raise ValidationError({
                "details": "Goal value has to be higher than 0"
            })

        return value


    def create(self, validated_data: dict):
        campaign = Campaign.objects.create(**validated_data)

        return campaign

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class DonationSerializer(serializers.Serializer):
    ong_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source="campaign.ong",
    )
    campaign_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source="campaign",
    )
    donation_id = serializers.UUIDField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source="user",
    )
    value = serializers.FloatField()

    def create(self, validated_data: dict):
        donation = Donation.objects.create(**validated_data)

        return donation
