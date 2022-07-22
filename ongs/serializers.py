from rest_framework import serializers

from ongs.models import Ong


class OngSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ong
        fields = [
            "ong_id",
            "name",
            "description",
            "cnpj",
            "site_address",
            "logo",
            "created_at",
        ]

    # TODO: add relations in serializers
    def create(self, validated_data: dict):
        return Ong.objects.create(**validated_data)

    def update(self, instance: Ong, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.site_address = validated_data.get(
            "site_address", instance.site_address
        )
        instance.logo = validated_data.get("logo", instance.logo)
        instance.save()
        return instance
