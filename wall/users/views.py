from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    BasePermission
)

from django.contrib.auth import get_user_model

from .serializers import UserSerializer

Users = get_user_model()

'''
class PostUserWritePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_superuser
'''


class UsersList(ListAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
