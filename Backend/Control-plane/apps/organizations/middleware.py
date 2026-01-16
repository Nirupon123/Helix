
from urllib import request
from django.http import Http404
from apps.organizations.models import Organization

class OrganizationContextMiddleware:
    """
    Attaches request.organization based on org_slug
    present in the URL.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        org_slug = request.resolver_match.kwargs.get("org_slug") \
            if request.resolver_match else None
        if org_slug:
            try:
                request.organization = Organization.objects.get(
                    slug=org_slug,
                    is_active=True
                )
            except Organization.DoesNotExist:
                raise Http404("Organization not found")
        else:
            request.organization = None

        return self.get_response(request)
    print("ORG MIDDLEWARE:", request.organization)

