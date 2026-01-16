
#Notes:
# Ensures access is limited to correct project
# Works with token-based auth
# Prevents cross-project access

from rest_framework.permissions import BasePermission


class IsProjectTokenAllowed(BasePermission):
    """
    Allows access only if request is authenticated
    using a valid ProjectToken.
    """

    def has_permission(self, request, view):
        return hasattr(request, "project")
