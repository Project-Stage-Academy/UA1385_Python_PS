from urllib import response
from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import StartupProfile, Subscription
from investors.models import InvestorProfile
from rest_framework_simplejwt.tokens import RefreshToken
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

class SubscriptionAPITest(APITestCase):

    def setUp(self):
        self.startup_user = User.objects.create_user(
            email="founder@example.com",
            password="StrongPass123!",
            user_name="founder",
            role=2
        )
        self.startup_profile = StartupProfile.objects.create(
            user_id=self.startup_user,
            title="Space Startup",
            description="We build rockets.",
            industry="Aerospace",
            website="https://startup.com",
            address="Moonbase Alpha"
        )

        self.investor_user = User.objects.create_user(
            email="investor@example.com",
            password="StrongPass123!",
            user_name="investor",
            role=1
        )
        self.investor_profile = InvestorProfile.objects.create(
            user_id=self.investor_user,
            company_name="InvestorCorp",
            address="Earth"
        )

        refresh = RefreshToken.for_user(self.investor_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.subscribe_url = reverse('startupprofile-subscribe', kwargs={'pk': self.startup_profile.startup_id})
        self.unsubscribe_url = reverse('startupprofile-unsubscribe', kwargs={'pk': self.startup_profile.startup_id})

        print(f"User active: {self.investor_user.is_active}")
        print(f"Access Token: {refresh.access_token}")

    def test_successful_subscription(self):
        response = self.client.post(self.subscribe_url)
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'subscribed')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_resubscribe_returns_already_subscribed(self):
        self.client.post(self.subscribe_url)  
        response = self.client.post(self.subscribe_url)  
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'already subscribed')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_successful_unsubscribe(self):
        self.client.post(self.subscribe_url)
        response = self.client.post(self.unsubscribe_url)
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unsubscribed')
        self.assertEqual(Subscription.objects.count(), 0)

    def test_unsubscribe_without_subscription(self):
        response = self.client.post(self.unsubscribe_url)
        print("Response status:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'not subscribed')