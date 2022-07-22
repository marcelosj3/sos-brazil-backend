from rest_framework.permissions import BasePermission
from rest_framework.views import Request


class IsSuperuser(BasePermission):
    def has_permission(self, request: Request, _):
        if request.user.is_superuser:
            return True
