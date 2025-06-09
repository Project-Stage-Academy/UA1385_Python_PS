from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User

class UserLoginTest(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "StrongPass123"
        User.objects.create_user(
            email = self.email, password = self.password,
            user_name = "testuser1", first_name = "Tom", last_name = "Tester"
        )
        self.url = reverse("token_obtain_pair")

    def test_login_success(self):
        response = self.client.post(self.url, {
            "email": self.email,
            "password": self.password
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            "email": self.email,
            "password": "wrong_pass"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
