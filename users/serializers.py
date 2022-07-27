from typing import OrderedDict

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework.authentication import authenticate
from sos_brazil.exceptions import (
    InvalidCredentialsException,
    InvalidKeyException,
    MissingKeyException,
)

from .models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attributes: dict):
        email = attributes.get("email", None)
        password = attributes.get("password", None)

        if not email or not password:
            raise InvalidCredentialsException()

        request = self.context.get("request")

        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise InvalidCredentialsException()

        attributes["user"] = user

        return attributes


class UserOngAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id"]


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

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: OrderedDict):
        return User.objects.create_user(**validated_data)

    def save_password(self, instance: User, password: str):
        setattr(instance, "password", make_password(password))
        instance.save()
        return instance

    def update_password(self, user: User, instance: User, validated_data: OrderedDict):
        """
        This function checks for an "password = True" property in the view
        in order to properly go on with the logic, if the view that requested
        the update does not have this property, it returns a False value.
        """
        update_password_view = self.context["view"].__class__.__dict__.get(
            "password", False
        )

        if not update_password_view:
            return False

        password = validated_data.get("password", None)
        old_password = self.context["request"]._data.get("old_password", None)

        is_superuser = user.__dict__.get("is_superuser", None)

        if is_superuser and password:
            return self.save_password(instance, password)

        if not old_password:
            raise MissingKeyException(
                "old_password",
                "in order to update the 'password', an 'old_password' key is necessary.",
            )

        if not check_password(old_password, user.password):
            raise InvalidCredentialsException()

        return self.save_password(instance, password)

    def update(self, instance: User, validated_data: OrderedDict):
        user: User = self.context["request"].user

        updated_password_instance = self.update_password(user, instance, validated_data)

        if updated_password_instance:
            return updated_password_instance

        if validated_data.get("password", None):
            raise InvalidKeyException(key="password")

        is_staff = validated_data.pop("is_staff", False)
        is_superuser = validated_data.pop("is_superuser", False)

        if user.is_superuser or user.is_staff:
            validated_data.setdefault("is_staff", is_staff)
            validated_data.setdefault("is_superuser", is_superuser)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
