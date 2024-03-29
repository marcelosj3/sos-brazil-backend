from typing import OrderedDict

from rest_framework import serializers

from campaigns.utils import check_dates
from sos_brazil.exceptions import GoalValueException, InvalidKeyException
from sos_brazil.settings import DATE_INPUT_FORMATS

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
    start_date = serializers.DateField(
        format=DATE_INPUT_FORMATS[0],
        input_formats=DATE_INPUT_FORMATS,
    )
    end_date = serializers.DateField(
        format=DATE_INPUT_FORMATS[0],
        input_formats=DATE_INPUT_FORMATS,
    )

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

    def donation(self, instance: Campaign, validated_data: OrderedDict):
        is_donation_view = self.context == "donation"

        if not is_donation_view:
            return False

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def end_campaign(self, instance: Campaign, validated_data: OrderedDict):
        is_end_campaign_view = self.context == "end_campaign"

        if not is_end_campaign_view:
            return False

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def update(self, instance: Campaign, validated_data: OrderedDict):
        if self.end_campaign(instance, validated_data):
            return instance

        if self.donation(instance, validated_data):
            return instance

        non_updatable_keys = ["collected", "goal_reached"]
        wrong_keys = []
        start_date = validated_data.get("start_date", instance.start_date)
        end_date = validated_data.get("end_date", instance.end_date)

        if start_date != instance.start_date or end_date != instance.end_date:
            check_dates(start_date, end_date)

        for key in validated_data.keys():
            if key in non_updatable_keys:
                wrong_keys.append(key)

        if wrong_keys:
            raise InvalidKeyException(
                message={"detail": "Cannot update key", "non_updatable": wrong_keys}
            )

        validated_data["goal_reached"] = bool(
            validated_data.get("goal", instance.goal) <= instance.collected
        )

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
