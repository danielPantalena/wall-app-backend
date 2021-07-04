from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core import mail


class AccountTests(APITestCase):
    def test_create_user(self):
        """
        Ensure anybody can create a new user.
        """
        url = reverse('users-list')
        data = {'username': 'xablau', 'password': '123',
                'email': 'xablau@xablau.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'xablau')

    def test_username_unique(self):
        """
        Ensure that usernames are unique.
        """
        url = reverse('users-list')
        data = {'username': 'daniel',
                'password': '4321', 'email': 'daniel@daniel.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(IntegrityError):
            self.client.post(url, data, format='json')

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

    def test_email_sender(self):
        """
        Ensure that the wellcome email is send.
        """
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            users_url = reverse('users-list')
            user_name = 'xablau'
            user_data = {'username': user_name, 'password': '123',
                         'email': 'xablau@xablau.com'}
            create_user_response = self.client.post(
                users_url, user_data, format='json')
            self.assertEquals(create_user_response.status_code,
                              status.HTTP_201_CREATED)
            self.assertEquals(len(mail.outbox), 1)
            self.assertEquals(
                mail.outbox[0].subject, f'Wellcome {user_name}! Your account was created at Wall App')
            self.assertEquals(
                mail.outbox[0].body, f'Hi, {user_name}. How are you? \n Now you can write a message on the Wall App after log in with your username {user_name} and the password that you created.')

    def test_generate_token(self):
        """
        Ensure we can generate token with username and password.
        """
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
