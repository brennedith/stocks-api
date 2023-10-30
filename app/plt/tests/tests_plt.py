from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestsPlt(APITestCase):
    def test_success_health_endpoint(self):
        url = reverse('plt:health')

        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data.get('data').get('status'), 'ok')