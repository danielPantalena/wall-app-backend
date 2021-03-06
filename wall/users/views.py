from django.http.response import JsonResponse
from rest_framework.generics import (
    ListCreateAPIView,
)
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from decouple import config
from .serializers import UserSerializer


class UsersList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        new_user_email = request.data['email']
        new_username = request.data['username']
        new_user_password = request.data['password']
        if not new_username or not new_user_email or not new_user_password:
            return JsonResponse({"Error": True, "message": "The fields: 'username', 'email' and 'password' are necessary", "example": {
                "username": "daniel",
                "email": "pantalenadaniel@gmail.com",
                "password": "xablau"
            }}, status=400)
        try:
            User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
            )
        except IntegrityError:
            return JsonResponse({"Error": True, "message": 'This username already exists. Please try another one :)'}, status=409)

        email_sender = config('EMAIL_SENDER')

        try:
            send_mail(
                f'Wellcome {new_username}! Your account was created at Wall App',
                f'Hi, {new_username}. How are you? \n Now you can write a message on the Wall App after log in with your username {new_username} and the password that you created.',
                f'Wall App <{email_sender}>',
                [request.data['email']],
                fail_silently=False,
            )
        except:
            print('SendGrid Error. Email not sended. Check the SENDGRIND_API_KEY and EMAIL_SENDER data')

        return JsonResponse({"created_user": request.data['username']}, status=201)
