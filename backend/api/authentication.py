from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.exceptions import AuthenticationFailed

from expiringtoken.models import ExpiringToken

class TokenAuthentication(BaseTokenAuth):
    keyword = "Bearer"

class ExpiringTokenAuthentication(BaseTokenAuth):
    keyword = "Bearer"
    model = ExpiringToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if token.is_expired():
            raise AuthenticationFailed('Token has expired.')

        return (token.user, token)

