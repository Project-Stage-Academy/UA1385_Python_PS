from django.test import TestCase

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import StartupProfile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class StartupProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password123!",
            user_name="testuser",
            first_name="Test",
            last_name="User",
            title="CEO",
            role=1, 
            user_phone="+380501234567"
        )

    def test_create_startup_profile(self):
        profile = StartupProfile.objects.create(
            user_id=self.user,
            title="My Startup",
            description="We build rockets.",
            industry="Aerospace",
            website="https://mystartup.com",
            address="123 Space Street"
        )
        self.assertEqual(profile.title, "My Startup")
        self.assertEqual(profile.user_id.email, "test@example.com")


class StartupProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="Password123!",
            user_name="testuser",
            first_name="Test",
            last_name="User",
            title="CEO",
            role=1, 
            user_phone="+380501234567"
        )


    def test_create_startup_profile_via_api(self):
        url = reverse('startupprofile-list')
 
        data = {
            "user_id": self.user.user_id,
            "title": "My API Startup",
            "description": "A test startup from API",
            "industry": "IT",
            "website": "https://api-startup.com",
            "address": "123 API Blvd"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "My API Startup")

