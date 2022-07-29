from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.permissions import IsSuperuserListCreateUser, IsSuperuserOrUser

from .serializers import UserLoginSerializer, UserSerializer


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuserListCreateUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserIdView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuserOrUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "user_id"


class UserIdPasswordView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuserOrUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = "user_id"

    password = True
