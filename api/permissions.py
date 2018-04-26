from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrUserReadOnly(BasePermission):
    """
    The request is authenticated as a admin, or is a user read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
