from rest_framework import permissions
from rest_framework import permissions
from users.models import CustomUser

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )

MODERATOR_METHODS = ('PATCH', 'DELETE')
class IsAuthorOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()
        if request.method in MODERATOR_METHODS:
            return (
                request.user == obj.author
                or request.user.role == 'moderator'
            )
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
        request.user.role == CustomUser.CustomUserRole.admin or
        request.user.is_superuser)
