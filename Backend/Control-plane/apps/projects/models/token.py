# apps/projects/models/token.py

# Notes:
# apps/projects/models/token.py
#Model representing a project within an organization.
#The Project and ProjectToken models are defined in the models package with\
#an __init__.py file to facilitate imports and work paralelly.


import secrets
from django.db import models
from apps.projects.models.project import Project


class ProjectToken(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tokens"
    )
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project} :: {self.name}"
