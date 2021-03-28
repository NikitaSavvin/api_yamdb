from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',  'email', 'bio', 'role', )
        model = CustomUser

        validators = [UniqueTogetherValidator(
            queryset=CustomUser.objects.all(),
            fields=['email',])]
