from dataclasses import fields

from rest_framework import serializers

from .models import Cause


class CauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cause
        fields = ["cause_id", "name"]
