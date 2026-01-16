

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.organizations.views import OrganizationViewSet
from rest_framework_nested.routers import NestedSimpleRouter

from apps.projects.views import ProjectViewSet, ProjectTokenViewSet

router = SimpleRouter()
router.register("", OrganizationViewSet, basename="organizations")

# organizations → projects
org_projects_router = NestedSimpleRouter(
    router,
    r"",
    lookup="org"
)
org_projects_router.register(
    r"projects",
    ProjectViewSet,
    basename="org-projects"
)

# projects → tokens
project_tokens_router = NestedSimpleRouter(
    org_projects_router,
    r"projects",
    lookup="project"
)
project_tokens_router.register(
    r"tokens",
    ProjectTokenViewSet,
    basename="project-tokens"
)

urlpatterns = router.urls + org_projects_router.urls + project_tokens_router.urls
