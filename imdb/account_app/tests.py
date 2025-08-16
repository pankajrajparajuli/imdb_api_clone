from urllib import response
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# Create your tests here.

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'testcase@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
            }
        self.client.post(reverse('api-register'), data, format='json')
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)
        



