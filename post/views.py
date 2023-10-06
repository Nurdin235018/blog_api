from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.permissions import *
from .models import Category, Tag, Post
from .serializers import CategorySerializer, TagSerializer, PostSerializer, PostListingSerializer
from rest_framework.response import Response


# class CategoryView(APIView):
#     def get(self, request):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data, status=200)
#
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)
#
#
# class CategoryDetailView(APIView):
#
#     def get_object(self, pk, http404=None):
#         try:
#             return Category.objects.get(slug=pk)
#         except Category.DoesNotExist:
#             return http404
#
#     def put(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(instance=category, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=206)
#
#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         category.delete()
#         return Response('Category successfully deleted', status=204)


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes = [AllowAny]
    #     elif self.request.method == 'POST':
    #         self.permission_classes = [IsAdminUser]
    #     return super().get_permissions()

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def get_permissions(self):
    #     if self.request.method in ('PUT', 'PATCH', 'DELETE'):
    #         self.permission_classes = [IsAdminUser]
    #     else:
    #           self.permission_classes = [AllowAny]
    #     return super().get_permissions()


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListingSerializer
        else:
            return self.serializer_class

