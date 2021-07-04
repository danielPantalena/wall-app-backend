from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer


class PostsList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('created_at').reverse()
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('created_at').reverse()
    permission_classes = [IsAuthenticatedOrReadOnly]
