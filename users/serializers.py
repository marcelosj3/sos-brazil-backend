from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "password",
            "created_at",
            "updated_at",
            "is_active",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        user: User = self.context["request"].user

        is_staff = validated_data.pop("is_staff", False)
        is_superuser = validated_data.pop("is_superuser", False)

        if user.is_superuser or user.is_staff:
            validated_data.setdefault("is_staff", is_staff)
            validated_data.setdefault("is_superuser", is_superuser)

        for key, value in validated_data.items():
            if key == "password":
                value = make_password(value)

            setattr(instance, key, value)

        instance.save()

        return instance
