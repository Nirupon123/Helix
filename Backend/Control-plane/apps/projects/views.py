from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from apps.projects.models import ProjectToken

from apps.projects.serializers import ProjectSerializer
from apps.projects.serializers import (
    ProjectTokenCreateSerializer,
    ProjectTokenReadSerializer,
)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field ="slug"

    def get_queryset(self):
        organization = self.request.organization
        return Project.objects.filter(
            organization=organization,
            is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)



class ProjectTokenViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProjectToken.objects.filter(
            project=self.project
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ProjectTokenCreateSerializer
        return ProjectTokenReadSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.project = self.get_project()

    def get_project(self):
        from apps.projects.models import Project

        return Project.objects.get(
            slug=self.kwargs["project_slug"],
            organization=self.request.organization
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"] = self.project
        return context