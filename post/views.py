from rest_framework.pagination import PageNumberPagination
# from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import *
from .models import Category, Tag, Post
from .serializers import CategorySerializer, TagSerializer, PostSerializer, PostListingSerializer
from preview.models import Like, Rating
from rest_framework.response import Response
from rest_framework.decorators import action
from preview.serializer import CommentSerializer, RatingSerializer


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

class PostSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['title']
    search_fields = ['title']
    pagination_class = PostSetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListingSerializer
        else:
            return self.serializer_class
    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author=user)
            like.save()
            message = 'liked'
        return Response(message)


    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    @action(['POST', 'PATCH'], detail=True)
    def rating(self, request, pk=None):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        rating = Rating.objects.filter(author=request.user, post=pk)
        serializer.is_valid(raise_exception=True)
        if rating and request.method == 'PATCH':
            serializer.update(rating[0], serializer.validated_data)
        elif rating and request.method == 'POST':
            return Response('You already had made a rating')
        elif not rating and request.mothod == 'POST':
            serializer.create(serializer.validated_data)
        return Response(serializer.data)

