from django.shortcuts import render
from .serializer import CommentSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Comment
from rest_framework.permissions import *


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
