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
from ongs.utils import check_cnpj_mask
from sos_brazil.exceptions import KeyTypeError, MissingKeyException

from .models import Ong


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


class OngIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOngOwner]

    def patch(self, request: Request, ong_id):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
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
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, _: Request, ong_id: str):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
            serialize = OngSerializer(ong)
            return Response(serialize.data, status.HTTP_200_OK)
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request: Request, ong_id):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
            self.check_object_permissions(request, ong)
            ong.delete()

            return Response("", status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)

        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)


class OngIdRegisterAdmin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOngOwner]

    def post(self, request: Request, ong_id: str):

        try:
            if not request.data.get("admins", False):
                raise MissingKeyException("admins", "This field is required.")
            request.data["admins"] = [
                {"user_id": user_id} for user_id in request.data["admins"]
            ]
            ong = get_object_or_404(Ong, pk=ong_id)
            self.check_object_permissions(request, ong)
            serialized = OngResgisterAdminSerializer(
                instance=ong, data=request.data, context={"request": request}
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)

        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request: Request, ong_id: str):
        try:
            if not request.data.get("admins", False):
                raise MissingKeyException("admins", "This field is required.")
            request.data["admins"] = [
                {"user_id": user_id} for user_id in request.data["admins"]
            ]
            ong = get_object_or_404(Ong, pk=ong_id)
            self.check_object_permissions(request, ong)
            serialized = OngRemoveAdminSerializer(
                instance=ong, data=request.data, context={"request": request}
            )
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(serialized.data, status.HTTP_200_OK)
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": err}, status.HTTP_422_UNPROCESSABLE_ENTITY)
