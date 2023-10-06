from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = self.Meta.model.objects.create(author=user, **validated_data)
        return comment
