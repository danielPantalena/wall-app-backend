from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'is_active', 'email']
