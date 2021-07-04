from logging import error
from django.http import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class AccountTests(APITestCase):

    def test_guests_can_read_messages(self):
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
