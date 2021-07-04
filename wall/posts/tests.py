from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class PostTests(APITestCase):
    def test_guests_can_read_posted_messages(self):
        """
        Ensure guests can read messages.
        """
        url = reverse('posts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_guests_can_not_post_message(self):
        """
        Ensure guests can not create a new message.
        """
        url = reverse('posts-list')
        data = {'title': 'some title', 'body': 'somebody :P'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_can_post_message(self):
        """
        Ensure logged in users can create messages.
        """
        users_url = reverse('users-list')
        user_data = {'username': 'mari',
                     'password': '4321', 'email': 'mari@mari.com'}
        created_response = self.client.post(
            users_url, user_data, format='json')
        self.assertEqual(created_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'mari')

        token_url = reverse('api-token-auth')
        token_data = {'username': 'mari', 'password': '4321'}
        token_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        user_token = token_response.data['token']
        posts_url = reverse('posts-list')
        post_data = {'title': 'some title', 'body': 'somebody :P'}
        post_response = self.client.post(
            posts_url, post_data, HTTP_AUTHORIZATION=f'Token {user_token}')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
