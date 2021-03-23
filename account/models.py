from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from account.managers import CustomUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return f'{self.email}'

    class Meta:
        db_table = 'account_custom_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    username = None  # this is to remove username from model
    email = models.EmailField(verbose_name=_('E-mail'), unique=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)