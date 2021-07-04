from logging import error
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class AccountTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('users-list')
        data = {'username': 'xablau', 'password': '123',
                'email': 'xablau@xablau.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'xablau')

    def test_email_validation(self):
        url = reverse('users-list')
        data = {'username': 'daniel',
                'password': '4321', 'email': 'daniel@'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['email'] = 'daniel@daniel.com'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['email'] = 'daniel@daniel'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_unique(self):
        url = reverse('users-list')
        data = {'username': 'daniel',
                'password': '4321', 'email': 'daniel@daniel.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(IntegrityError):
            self.client.post(url, data, format='json')

    def test_generate_token(self):
        users_url = reverse('users-list')
        user_data = {'username': 'mari',
                     'password': '4321', 'email': 'mari@mari.com'}
        created_response = self.client.post(
            users_url, user_data, format='json')
        self.assertEqual(created_response.status_code, status.HTTP_201_CREATED)
        token_url = reverse('api-token-auth')
        token_data = {'username': 'mari', 'password': '54321'}
        bad_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        token_data = {'username': 'mari', 'password': '4321'}
        ok_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(ok_response.status_code, status.HTTP_200_OK)
