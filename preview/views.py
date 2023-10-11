from django.shortcuts import render
from rest_framework import generics
from .serializer import CommentSerializer, RatingSerializer, LikeSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Rating, Like
from rest_framework.permissions import *
from .permissions import IsAuthorPermission


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()


class LikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

