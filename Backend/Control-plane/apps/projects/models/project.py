
# Notes:
#apps/projects/models/project.py
#Model representing a project within an organization.
#The Project and ProjectToken models are defined in the models package with\
#an __init__.py file to facilitate imports and work paralelly.



from django.db import models
from django.utils.text import slugify
from apps.organizations.models import Organization


class Project(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "slug")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Project.objects.filter(
                organization=self.organization,
                slug=slug
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organization.slug}/{self.slug}"
