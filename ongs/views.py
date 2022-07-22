from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status

from ongs.serializers import OngSerializer

from .models import Ong

# Create your views here.


class OngView(APIView):
    def get(self, _: Request):
        ongs = Ong.objects.all()
        serialized = OngSerializer(instance=ongs, many=True)
        return Response({ongs: serialized.data}, status.HTTP_200_OK)
