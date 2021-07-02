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
        is_email_valid = re.match(r"^\w+@\w+\.[a-z]{2,}", new_user_email)
        if not is_email_valid:
            return HttpResponseBadRequest('A field with a valid email is necessary')

        # send_mail(
        #     'Congratulations! Your user - {} - was created at Wall App'.format(
        #         request.data['username']),
        #     'Hello {} {}, now you can login at Wall App using username and password that you created.'.format(
        #         'hi', 'last_name'),
        #     'Wall App',
        #     [request.data['email']],
        #     fail_silently=False,
        # )
        return HttpResponse(request.data['email'])
