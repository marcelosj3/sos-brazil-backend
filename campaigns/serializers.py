from rest_framework import serializers
from sos_brazil.exceptions import CampaignDateException, GoalValueException
from sos_brazil.settings import DATE_INPUT_FORMATS

from campaigns.utils import check_dates

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
    start_date = serializers.DateField(input_formats=DATE_INPUT_FORMATS)
    end_date = serializers.DateField(input_formats=DATE_INPUT_FORMATS)

    def validate_goal(self, value):
        if value <= 0:
            raise GoalValueException()

        return value

    def create(self, validated_data: dict):
        start_date = validated_data.get("start_date", None)
        end_date = validated_data.get("end_date", None)

        check_dates(start_date, end_date)

        campaign = Campaign.objects.create(**validated_data)

        return campaign

    def update(self, instance, validated_data):
        non_updatable_keys = ["collected", "goal_reached"]
        wrong_keys = []
        start_date = validated_data.get("start_date", instance.start_date)
        end_date = validated_data.get("end_date", instance.end_date)

        if start_date >= end_date:
            raise CampaignDateException()

        check_dates(start_date, end_date)

        for key in validated_data.keys():
            if key in non_updatable_keys:
                wrong_keys.append(key)

        if wrong_keys:
            raise KeyError(f"Cannot update the key(s): {wrong_keys}")

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
