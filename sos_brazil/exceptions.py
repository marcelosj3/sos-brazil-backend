from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidCredentialsException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials."


class MissingKeyException(APIException):
    default_detail = "Missing keys."

    def __init__(
        self,
        key: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.detail = {key.lower(): message}
        self.status_code = status_code


class InvalidKeyException(APIException):
    default_detail = "Cannot update this key."

    def __init__(
        self,
        key: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.detail = f"{key.title()} cannot be updated."
        self.status_code = status_code


class KeyTypeError(APIException):
    default_detail = "Expected a list of items"

    def __init__(
        self,
        key: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.detail = {key.lower(): message}
        self.status_code = status_code
