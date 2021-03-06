from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer
from .permisions import IsOwnerOrReadOnly


class PostsList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('created_at').reverse()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('created_at').reverse()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
