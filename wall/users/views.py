from django.http.response import HttpResponse, JsonResponse
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from django.core.mail import send_mail
import re
from decouple import config


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
    permission_classes = [AllowAny]

    def post(self, request):
        new_user_email = request.data['email']
        new_username = request.data['username']
        is_email_valid = re.match(r"^[\w\.]+@\w+\.[a-z]{2,}", new_user_email)
        if not is_email_valid:
            return JsonResponse({"Error": True, "message": 'A field with a valid email is necessary'}, status=400)

        User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
        )

        email_sender = config('EMAIL_SENDER')

        send_mail(
            f'Wellcome {new_username}! Your account was created at Wall App',
            f'Congratulations {new_username}, now you can login at Wall App using your username {new_username} and the password that you created.',
            f'Wall App <{email_sender}>',
            [request.data['email']],
            fail_silently=False,
        )

        return JsonResponse({"created_user": request.data['username']}, status=201)
