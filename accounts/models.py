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

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name and not self.last_name:
            return self.first_name
        elif not self.first_name and self.last_name:
            return self.last_name
        else:
            return self.email
