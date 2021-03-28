from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class CustomUserRole(models.TextChoices):
        admin = 'admin'
        user = 'user'
        moderator ='moderator'

    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField(('User_status'), max_length=20,
                            choices=CustomUserRole.choices,
                            default=CustomUserRole.user)
    confirmation_code = models.CharField(max_length=20)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_moderator(self):
        return self.role == 'moderator'
