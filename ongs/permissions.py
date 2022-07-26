# def has_object_permission
from rest_framework.permissions import BasePermission
from rest_framework.views import Request

from ongs.models import Ong


class isOngOwner(BasePermission):
    def has_object_permission(self, request: Request, _, obj: Ong):
        owner_method = {"PATCH", "DELETE"}
        for request.method in owner_method:
            return True
        for owner in obj.admins:
            return owner == request.user
