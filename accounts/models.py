from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django_use_email_as_username.models import BaseUser, BaseUserManager


class User(BaseUser):
    email = models.EmailField(  # type: ignore
        verbose_name=_('e-mail'),
        unique=True,
    )
    phone = PhoneNumberField(
        verbose_name=_('Phone Number'),
    )

    objects = BaseUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
