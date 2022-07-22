from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserLoginSerializer


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer
