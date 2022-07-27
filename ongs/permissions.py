from rest_framework.permissions import BasePermission
from rest_framework.views import Request

from ongs.models import Ong


class isOngOwner(BasePermission):
    def has_permission(self, request, view):
        admin_methods = {"POST", "PATCH", "DELETE"}
        if request.method in admin_methods:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request: Request, view, obj: Ong):
        owner_method = {"PATCH", "DELETE"}
        for request.method in owner_method:
            if request.user.__dict__["user_id"] in obj.admins.values():
                return True
        return False
