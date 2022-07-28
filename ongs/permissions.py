from rest_framework.permissions import BasePermission
from rest_framework.views import Request

from ongs.models import Ong


class isOngOwner(BasePermission):
    def has_permission(self, request, _):
        admin_methods = {"POST", "PATCH", "DELETE"}
        if request.method in admin_methods:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request: Request, _, obj: Ong):
        owner_method = {"PATCH", "DELETE"}
        for request.method in owner_method:
            authorized = False

            for admin in obj.admins.values():
                if request.user.user_id == admin["user_id"]:
                    authorized = True
                    break

            return authorized
