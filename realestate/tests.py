from django.test import TestCase, Client
from django.urls import reverse


class RealestateHomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_status_code(self):
        response = self.client.get(reverse('realestate:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('realestate:home'))
        self.assertTemplateUsed(response, 'realestate/home.html')
