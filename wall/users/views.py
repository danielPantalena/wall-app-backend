from django.http.response import JsonResponse
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from django.core.mail import send_mail
import re
from decouple import config


from .serializers import UserSerializer


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
            f'Hi, {new_username}. How are you? \n Now you can write a message on the Wall App after log in with your username {new_username} and the password that you created.',
            f'Wall App <{email_sender}>',
            [request.data['email']],
            fail_silently=False,
        )

        return JsonResponse({"created_user": request.data['username']}, status=201)
