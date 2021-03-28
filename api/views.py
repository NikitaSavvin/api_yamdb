from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action

from .permissions import IsAdminOrSuperUser
from users.models import CustomUser
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser,]
    lookup_field = "username"

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid() and user.username == request.user.username:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
