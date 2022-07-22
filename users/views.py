from rest_framework.generics import ListCreateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
