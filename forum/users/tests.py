from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User

class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.payload = {
            "email": "test@example.com",
            "password": "StrongPass123",
            "user_name": "testuser1",
            "first_name": "Tom",
            "second_name": "Tester",
            "role": 1,
        }
        self.url = reverse("register")
    
    def test_create_user_via_registration_endpoint(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(email=self.payload["email"]).exists())
        
        user = User.objects.get(email=self.payload["email"])
        self.assertEqual(user.user_name, self.payload["user_name"])
        self.assertEqual(user.first_name, self.payload["first_name"])
        self.assertTrue(user.check_password(self.payload["password"]))
