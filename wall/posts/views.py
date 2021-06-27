from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    BasePermission
)

from .models import Post
from .serializers import PostSerializer

'''
class PostUserWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser
'''

class PostsList(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('created_at').reverse()
    

class PostDetails(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated, PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

''' Concrete View Classes
    # CreateAPIView
        Used for create-only endpoints.
    # ListAPIView
        Used for read-only endpoints to represent a collection of model instances.
    # RetrieveAPIView
        Used for read-only endpoints to represent a single model instance.
    # DestroyAPIView
        Used for delete-only endpoints for a single model instance.
    # UpdateAPIView
        Used for update-only endpoints for a single model instance.
    # ListCreateAPIView
        Used for read-write endpoints to represent a collection of model instances.
    # RetrieveUpdateAPIView
        Used for read or update endpoints to represent a single model instance.
    # RetrieveDestroyAPIView
        Used for read or delete endpoints to represent a single model instance.
    # RetrieveUpdateDestroyAPIView
        Used for read-write-delete endpoints to represent a single model instance.
'''
