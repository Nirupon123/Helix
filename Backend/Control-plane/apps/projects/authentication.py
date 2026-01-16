
#Notes:
# Reads Authorization: Bearer <token>
# Validates token
# Attaches:
# request.project
# request.organization
# No user login needed

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from apps.projects.models import ProjectToken


class ProjectTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self,request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # allow other auth methods
        try:
            keyword,token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format")

        if keyword !=self.keyword:
            return None
        try:
            project_token =ProjectToken.objects.select_related(
                "project",
                "project__organization"
            ).get(key=token, 
                  is_active=True)
            
        except ProjectToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive project token")

        # update last used timestamp
        project_token.last_used_at = timezone.now()
        project_token.save(update_fields=["last_used_at"])

        # Attach context to request
        request.project = project_token.project
        request.organization = project_token.project.organization

        # No user, token-based auth
        return (None, project_token)
