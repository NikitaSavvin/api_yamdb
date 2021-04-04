from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_confirmation_code


class CustomUser(AbstractUser):

    class CustomUserRole(models.TextChoices):
        admin = 'admin'
        user = 'user'
        moderator = 'moderator'

    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField('User_status', max_length=20,
                            choices=CustomUserRole.choices,
                            default=CustomUserRole.user)
    confirmation_code = models.CharField(max_length=100, null=True,
                                         verbose_name='Код подтверждения',
                                         default=generate_confirmation_code())
    email = models.EmailField(max_length=255, unique=True,
                              blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'
