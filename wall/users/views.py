from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    BasePermission
)

from django.contrib.auth.models import User
from django.core.mail import send_mail
import re

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

    def post(self, request):
        new_user_email = request.data['email']
        new_user_name = request.data['username']
        is_email_valid = re.match(r"^[\w\.]+@\w+\.[a-z]{2,}", new_user_email)
        if not is_email_valid:
            return HttpResponseBadRequest('A field with a valid email is necessary')

        send_mail(
            f'Congratulations {new_user_name}! Your account was created at Wall App',
            f'Hello {new_user_name}, now you can login at Wall App using your email {new_user_email} and the password that you created.',
            'Wall App <pantalenadaniel@gmail.com>',
            [request.data['email']],
            fail_silently=False,
        )
        return HttpResponse(request.data['email'])
