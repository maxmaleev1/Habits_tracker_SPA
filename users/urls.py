from django.urls import path
from .apps import UsersConfig
from .views import UserCreateAPIView, TokenObtainPairView, TokenRefreshView


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
]
