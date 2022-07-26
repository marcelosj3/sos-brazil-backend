from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User

from .serializers import UserLoginSerializer, UserSerializer


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserIdPasswordView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    # TODO add only superuser and user itself permission
    permission_classes = [IsAuthenticated]

    password = True

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "user_id"
