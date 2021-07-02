from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    BasePermission
)

from django.contrib.auth.models import User

from .serializers import UserSerializer

'''
class PostUserWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser
'''


class UsersList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
