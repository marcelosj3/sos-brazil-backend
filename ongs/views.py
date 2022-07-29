from curses.ascii import HT

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status

from ongs.permissions import IsOngOwner
from ongs.serializers import (
    OngRemoveAdminSerializer,
    OngResgisterAdminSerializer,
    OngSerializer,
)
from sos_brazil.exceptions import (
    IncorrectUUIDException,
    KeyTypeError,
    MissingKeyException,
    NotFoundException,
)
from users.models import User

from .models import Ong


class OngGenericView(APIView):
    def get_ong_or_404(self, ong_id: str):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
            return ong
        except Http404:
            raise NotFoundException("ong")
        except ValidationError:
            raise IncorrectUUIDException


class OngView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request):
        causes = request.data.get("causes", False)

        if not causes:
            raise MissingKeyException("causes", "This field is required.")

        if not isinstance(causes, list):
            raise KeyTypeError(key="causes", message="Expect a list of items")

        request.data["causes"] = [{"name": cause} for cause in request.data["causes"]]
        serialized = OngSerializer(data=request.data, context={"request": request})
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status.HTTP_201_CREATED)

    def get(self, _: Request):
        ongs = Ong.objects.all()
        serialized = OngSerializer(instance=ongs, many=True)
        return Response({"ongs": serialized.data}, status.HTTP_200_OK)


class OngIdView(OngGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOngOwner]

    def patch(self, request: Request, ong_id):
        ong = self.get_ong_or_404(ong_id)

        self.check_object_permissions(request, ong)

        causes = request.data.get("causes", False)
        if causes:
            if not isinstance(causes, list):
                raise KeyTypeError(key="causes", message="Expect a list of items")
            request.data["causes"] = [
                {"name": cause} for cause in request.data["causes"]
            ]

        serialized = OngSerializer(instance=ong, data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_200_OK)

    def get(self, _: Request, ong_id: str):
        ong = self.get_ong_or_404(ong_id)
        serialize = OngSerializer(ong)
        return Response(serialize.data, status.HTTP_200_OK)

    def delete(self, request: Request, ong_id):
        ong = self.get_ong_or_404(ong_id)
        self.check_object_permissions(request, ong)
        ong.delete()
        return Response("", status.HTTP_204_NO_CONTENT)


class OngIdManageAdmins(OngGenericView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOngOwner]

    def check_for_admins(self, request):
        if not request.data.get("admins", False):
            raise MissingKeyException("admins", "This field is required.")

        try:
            for user_id in request.data["admins"]:
                user = get_object_or_404(User, pk=user_id)
                if not user:
                    raise Http404()

            request.data["admins"] = [
                {"user_id": user_id} for user_id in request.data["admins"]
            ]

        except Http404:
            raise NotFoundException("user")

        return request

    def post(self, request: Request, ong_id: str):
        try:
            request = self.check_for_admins(request)
            ong = self.get_ong_or_404(ong_id)
            self.check_object_permissions(request, ong)
            serialized = OngResgisterAdminSerializer(
                instance=ong, data=request.data, context={"request": request}
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request: Request, ong_id: str):
        try:
            request = self.check_for_admins(request)
            ong = self.get_ong_or_404(ong_id)
            self.check_object_permissions(request, ong)
            serialized = OngRemoveAdminSerializer(
                instance=ong, data=request.data, context={"request": request}
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)
