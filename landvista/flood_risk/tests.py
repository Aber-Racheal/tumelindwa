from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FloodRisk

class FloodRiskAPITests(APITestCase):
    def setUp(self):
        self.create_url = reverse('flood-risk-predict')
        self.get_url = lambda location: reverse('flood-risk', kwargs={'location': location})

    def test_create_flood_risk(self):
        data = {
            "location": "Dandora",
            "risk_percentage": 30.0,
            "soil_type": "Clay",
            "elevation": 150.0
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flood_risk_case_insensitive(self):
        data = {
            "location": "dandora",
            "risk_percentage": 40.0,
            "soil_type": "Clay",
            "elevation": 150.0
        }
        # First create
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Now update with different case
        updated_data = {
            "location": "DANDORA",
            "risk_percentage": 50.0,
            "soil_type": "Sandy",
            "elevation": 200.0
        }
        response = self.client.post(self.create_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Should update

        # Check if the data was updated correctly
        flood_risk = FloodRisk.objects.get(location__iexact="dandora")
        self.assertEqual(flood_risk.risk_percentage, 50.0)
        self.assertEqual(flood_risk.soil_type, "Sandy")
        self.assertEqual(flood_risk.elevation, 200.0)

    def test_get_flood_risk_case_insensitive(self):
        data = {
            "location": "Dandora",
            "risk_percentage": 30.0,
            "soil_type": "Clay",
            "elevation": 150.0
        }
        self.client.post(self.create_url, data, format='json')

        response = self.client.get(self.get_url("DANDORA"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], "Dandora")

    def test_get_flood_risk_not_found(self):
        response = self.client.get(self.get_url("UnknownLocation"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
