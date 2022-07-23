from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import Request


class IsSuperuserListCreateUser(IsAuthenticated, BasePermission):
    """
    This permission is used to required authentication and
    superuser credentials in order to list all users. Regarding
    creating an user, this permission will allow freely.
    """

    SAFE_METHODS = ["POST"]

    def has_permission(self, request: Request, _):
        if request.method in self.SAFE_METHODS:
            return True

        return bool(request.user.is_superuser and request.method == "GET")
