from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status

from ongs.serializers import OngSerializer

from .models import Ong

# Create your views here.


class OngView(APIView):
    def get(self, _: Request):
        ongs = Ong.objects.all()
        serialized = OngSerializer(instance=ongs, many=True)
        return Response({ongs: serialized.data}, status.HTTP_200_OK)


class OngIdView(APIView):
    def get(self, _: Request, ong_id: int):
        try:
            ong = get_object_or_404(Ong, pk=ong_id)
            serialize = OngSerializer(ong)
            return Response(serialize.data, status.HTTP_200_OK)
        except Http404:
            return Response({"Error": "Ong Not Found"}, status.HTTP_404_NOT_FOUND)
