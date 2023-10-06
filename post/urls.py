from django.urls import path, include
from .views import CategoryView, CategoryDetailView, TagView, TagDetailView, PostView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostView)


urlpatterns = [
    path('categories/', CategoryView.as_view()),
    path('categories/<slug:pk>/', CategoryDetailView.as_view()),
    path('tags/', TagView.as_view()),
    path('tags/<slug:pk>/', TagDetailView.as_view()),
    path('', include(router.urls))
    # path('posts/', PostView.as_view({'get': 'list', 'post': 'create'})),
    # path('posts/<int:pk>/', PostView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
    #                                           'delete': 'destroy'}))
]
