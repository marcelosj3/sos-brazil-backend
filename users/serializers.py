from rest_framework import serializers
from rest_framework.authentication import authenticate

from sos_brazil.exceptions import InvalidCredentialsException


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attributes):
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
