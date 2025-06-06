from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from .models import User
from .serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class TokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)
