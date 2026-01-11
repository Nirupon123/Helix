from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Organization, OrganizationMember
from .serializers import OrganizationSerializer



class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        """using ' __ 'go through a 
          relationship and related_name 
          in models set is 'members' so it 
          can access the members using 
          that related name"""
        return Organization.objects.filter(
            members__user=self.request.user, 
            members__is_active=True,   
            is_active=True,
        ).distinct()

    def perform_create(self, serializer):
        """
        Creating org with owner membership.
        """
        org = serializer.save(owner=self.request.user)

        OrganizationMember.objects.create(
            organization=org,
            user=self.request.user,
            role="owner",
        )

    def perform_update(self, serializer):
        """
        Update org metadata (name, settings).
        Requires manage_org permission.
        """
        org = self.get_object()

        member = get_object_or_404(
            OrganizationMember,
            organization=org,
            user=self.request.user,
            is_active=True,
        )

        if not member.has_permission("manage_org"):
            raise PermissionDenied("You cannot manage this organization.")

        serializer.save()

    def perform_destroy(self, instance):
        """
        Soft delete organization.
        Requires manage_org permission.
        """
        org = self.get_object()

        member = get_object_or_404(
            OrganizationMember,
            organization=org,
            user=self.request.user,
            is_active=True,
        )

        if not member.has_permission("manage_org"):
            raise PermissionDenied("You cannot manage this organization.")

        instance.is_active = False
        instance.save()
