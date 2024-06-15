from rest_framework.permissions import BasePermission


class IsActiveEmployeePermission(BasePermission):
    """Class for checking if user is active employee."""

    def has_permission(self, request, view):
        return request.user.is_active
