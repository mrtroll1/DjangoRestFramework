import binascii
import os
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ExpiringToken(models.Model):
    """
    Mimics the default authorization token model (Token) + adds 'expires' feature
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='expiringtoken',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(blank=True, null=True) # New feature

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = False
        verbose_name = _("ExpiringToken")
        verbose_name_plural = _("ExpiringTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.created = timezone.now()
        if not self.expires:
            self.expires = self.created + settings.TOKEN_EXPIRATION_TIME
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() >= self.expires

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    
class ExpiringTokenProxy(ExpiringToken):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user_id

    class Meta:
        proxy = 'expiringtoken' in settings.INSTALLED_APPS
        abstract = 'expiringtoken' not in settings.INSTALLED_APPS
        verbose_name = _("ExpiringToken")
        verbose_name_plural = _("ExpiringTokens")

