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
        key: str = "",
        message: str = "",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if not message:
            self.detail = f"{key.title()} cannot be updated."
        else:
            self.detail = message
        self.status_code = status_code


class GoalValueException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Goal value has to be higher than 0"


class InvalidFormatException(APIException):
    default_detail = "Invalid format."

    def __init__(
        self,
        messages: dict,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.detail = messages
        self.status_code = status_code


class CampaignDateException(APIException):
    default_detail = "The start_date can't be later to the end_date or contrariwise."

    def __init__(
        self,
        messages: dict,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.detail = {"detail": self.default_detail, "dates": messages}
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


class MinimumAdminValueException(APIException):
    default_detail = "Minimum one admin required."

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_404_NOT_FOUND,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.detail = message
        self.status_code = status_code


class NotFoundException(APIException):
    def __init__(
        self,
        instance_name: str,
        status_code: int = status.HTTP_404_NOT_FOUND,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.detail = f"{instance_name.title()} not found."
        self.status_code = status_code


class IncorrectUUIDException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Incorrect UUID format received"


class WrongValueException(APIException):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.detail = message
        self.status_code = status_code
