from rest_framework import serializers

from causes.models import Cause
from causes.serializers import CauseSerializer
from ongs.models import Ong
from ongs.utils import check_cnpj_mask
from sos_brazil.exceptions import MinimumAdminValueException
from users.serializers import UserOngAdminSerializer


class OngSerializer(serializers.ModelSerializer):
    causes = CauseSerializer(many=True)

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
            "causes",
        ]

    def validate_cnpj(self, value):
        if check_cnpj_mask(value):
            return value

    def create(self, validated_data: dict):
        admin = self.context["request"].user
        causes = validated_data.pop("causes")
        ong = Ong.objects.create(**validated_data)

        for cause in causes:
            cause, _ = Cause.objects.get_or_create(**cause)
            ong.causes.add(cause)

        ong.admins.add(admin)

        return ong

    def update(self, instance: Ong, validated_data: dict):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.cnpj = validated_data.get("cnpj", instance.cnpj)
        instance.site_address = validated_data.get(
            "site_address", instance.site_address
        )
        instance.logo = validated_data.get("logo", instance.logo)
        instance.save()
        return instance


class OngResgisterAdminSerializer(serializers.Serializer):
    admins = UserOngAdminSerializer(many=True)

    class Meta:
        model = Ong
        fields = ["admins"]

    def update(self, instance: Ong, _: dict):
        admins = self.context["request"].data
        for admin in admins["admins"]:
            instance.admins.add(admin["user_id"])
        instance.save()

        return instance


class OngRemoveAdminSerializer(serializers.Serializer):
    admins = UserOngAdminSerializer(many=True)

    class Meta:
        model = Ong
        fields = ["admins"]

    def update(self, instance: Ong, _: dict):
        admins = self.context["request"].data
        for admin in admins["admins"]:
            if len(instance.admins.values()) > 1:
                instance.admins.remove(admin["user_id"])
            else:
                raise MinimumAdminValueException(
                    message="Minimum one admin is required."
                )
        instance.save()

        return instance
