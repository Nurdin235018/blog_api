from rest_framework import serializers

from preview.serializer import CommentSerializer
from .models import Category, Tag, Post


# class CategorySerializer(serializers.Serializer):
#     title = serializers.CharField(required=True, max_length=40)
#     slug = serializers.SlugField(required=False)
#
#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.save()
#         return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('title',)


# class PostSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Post
#         fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags', [])
        post = self.Meta.model.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return rep


class PostListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image',)
