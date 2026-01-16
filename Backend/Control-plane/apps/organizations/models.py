from django.conf import settings
from django.db import models
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


class Organization(models.Model):

    name = models.CharField(max_length=255)

    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owned_organization"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Organization.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    DEFAULT_SETTINGS = {
        "snapshots_enabled": True,
        "replay_enabled": True,
        "capture_headers": True,
        "capture_request_body": False,
        "default_incident_severity": "medium",
    }

    def get_setting(self, key):
        return self.settings.get(
            key,
            self.DEFAULT_SETTINGS.get(key)
        )

    def is_snapshot_enabled(self):
        return self.get_setting("snapshots_enabled")

    def is_replay_enabled(self):
        return self.get_setting("replay_enabled")

    


class OrganizationMember(models.Model):

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organization_memberships"
    )

    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("developer", "Developer"),
        ("viewer", "Viewer"),
    )
    # Coarse-grained role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="viewer"
    )
    # Fine grained permissions
    permissions = models.JSONField(default=dict, blank=True)

    # Membership lifecycle
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "user") # Prevent duplicate user permissions
        ordering = ["joined_at"]

    def __str__(self):
        return f"{self.user} of {self.organization}"

    # Permission helpers
    def has_permission(self, perm_name):
        if perm_name in self.permissions:
            return self.permissions[perm_name]
        

        ROLE_DEFAULTS = {
            "owner": True,
            "admin": True,
            "developer": perm_name != "manage_org",
            "viewer": False,
        }

        return ROLE_DEFAULTS.get(self.role, False)

