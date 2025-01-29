from rest_framework import serializers
from backend.models import Forum


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
        }

    def validate_name(self, value):
        """
        ✅ Allows updating an existing forum without triggering the unique constraint.
        ✅ Prevents duplicate forum names when creating a new one.
        """
        if self.instance:  # ✅ Check if updating an existing forum
            if Forum.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Forum with this name already exists.")
        else:  # ✅ Check for duplicates when creating a new forum
            if Forum.objects.filter(name=value).exists():
                raise serializers.ValidationError("Forum with this name already exists.")
        
        return value