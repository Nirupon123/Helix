#Create token
#POST /api/projects/{project_slug}/tokens/

#List tokens
#GET /api/projects/{project_slug}/tokens/



from rest_framework import serializers
from apps.projects.models import Project, ProjectToken


class ProjectSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ["id","organization","name","slug","is_active","created_at"]
        read_only_fields = ["organization"]

class ProjectTokenCreateSerializer(serializers.ModelSerializer):
    key = serializers.CharField(read_only=True)
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = ProjectToken
        fields = ["id","name","key","is_active","created_at"]
        read_only_fields = ["is_active"]

    def create(self, validated_data):
        project = self.context["project"]
        return ProjectToken.objects.create(
            project=project,
            **validated_data
        )
    
class ProjectTokenReadSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    last_used_at = serializers.ReadOnlyField()

    class Meta:
        model = ProjectToken
        fields = ["id","name","is_active","created_at","last_used_at"]



