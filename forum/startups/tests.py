from rest_framework.test import APITestCase
from users.models import User
from startups.models import Startup
import uuid

class StartupAPITest(APITestCase):
    def setUp(self):
        unique_email = f"{uuid.uuid4()}@example.com"
        self.investor = User.objects.create_user(email=unique_email, password='random123456789', role=1)
        self.client.force_authenticate(user=self.investor)
        self.startup = Startup.objects.create(user_id=self.investor, title="Start 1", description="Start 1", industry="AI",
                               company_size="50", website="test-test.ua", address="Dnipro, Ukraine")

    def test_can_view_startup_list(self):
        response = self.client.get('/api/startups/')
        self.assertEqual(response.status_code, 200)

    def test_can_view_startup_detail(self):
        startup = Startup.objects.create(
            user_id=self.investor,
            title="GreenAI",
            description="AI solutions",
            industry="AI",
            company_size=50,
            website="https://greenai.example.com",
            address="Kyiv, Ukraine"
        )

        response = self.client.get(f'/api/startups/{self.startup.startup_id}/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['title'], "GreenAI")

        self.assertEqual(response.data['industry'], "AI")

    def test_can_filter_by_investment_needs(self):
        Startup.objects.create(
            user_id=self.investor,
            title="Startup A",
            description="Desc A",
            industry="Finance",
            company_size=10,
            website="https://startup-a.example.com",
            address="Kyiv"
        )

        Startup.objects.create(
            user_id=self.investor,
            title="Startup B",
            description="Desc B",
            industry="Health",
            company_size=20,
            website="https://startup-b.example.com",
            address="Lviv"
        )

        response = self.client.get('/api/startups/?investment_needs=True')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['title'], "Startup A")

    def test_can_search_startup_by_title(self):
        Startup.objects.create(
            user_id=self.investor,
            title="Soft Serve",
            description="AI solutions",
            industry="AI",
            company_size=30,
            website="https://ss.example.com",
            address="Kyiv"
        )

        Startup.objects.create(
            user_id=self.investor,
            title="BlueOcean",
            description="Maritime technologies",
            industry="Marine",
            company_size=15,
            website="https://blueocean.example.com",
            address="Odessa"
        )

        response = self.client.get('/api/startups/?search=GreenAI')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['title'], "GreenAI")
