from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from ongs.serializers import OngSerializer

from .models import Ong


class OngView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, _: Request):
        ongs = Ong.objects.all()
        serialized = OngSerializer(instance=ongs, many=True)
        return Response({"ongs": serialized.data}, status.HTTP_200_OK)

    def post(self, request: Request):
        serialized = OngSerializer(data=request.data)
        serialized.is_valid()
        serialized.save()
        return Response(serialized.data, status.HTTP_201_CREATED)


class OngIdView(APIView):
    def get(self, _: Request, ong_id: str):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
            serialize = OngSerializer(ong)
            return Response(serialize.data, status.HTTP_200_OK)
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, ong_id):
        ong = get_object_or_404(Ong, pk=ong_id)

        serialized = OngSerializer(instance=ong, data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, response: Response, ong_id):
        ong = get_object_or_404(Ong, pk=ong_id)

        ong.delete()

        return Response("", status.HTTP_204_NO_CONTENT)
