from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListCreateAPIView

from users.models import User

from .serializers import UserLoginSerializer, UserSerializer


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
