from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# from rest_framework.authtoken.views import obtain_auth_token # we have overriden the ObtainTokenAuth class to use ExpiringToken model

from . import views
from expiringtoken.views import obtain_expiring_auth_token

urlpatterns = [
    path('', views.api_home),
    path('auth/', obtain_expiring_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
