from rest_framework import permissions

from users.models import CustomUserRole


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == request.user.is_admin
                or request.user.is_superuser))


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == CustomUserRole.admin
            or request.user.role == CustomUserRole.moderator
        )


class IsAdminOrSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == CustomUserRole.admin
                or request.user.is_superuser)
