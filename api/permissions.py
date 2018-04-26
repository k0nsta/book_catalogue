from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrUserReadOnly(BasePermission):
    def has_object_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj.
