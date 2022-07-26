from rest_framework import serializers, status

from .models import Cause


class CauseSerializer(serializers.Serializer):

    cause_id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data: dict):
        cause, created = Cause.objects.get_or_create(**validated_data)
        if not created:
            raise ValueError(
                {"message": f"`{validated_data['name']}` already exists."},
                status.HTTP_409_CONFLICT,
            )
        return cause
