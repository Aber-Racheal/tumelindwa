from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import FloodRisk
import json

class FloodRiskAPITests(APITestCase):
    def setUp(self):
        self.valid_data = {
            "location": "Test Location",
            "risk_percentage": {
                "short_rains": 30,
                "long_rains": 20,
                "short_dry_season": 5,
                "long_dry_season": 10
            },
            "soil_type": "Clay",
            "elevation": 150.0
        }
        self.url_predict = reverse('flood-risk-predict')
        self.url_retrieve = reverse('flood-risk', args=["Test Location"])

    def test_create_flood_risk(self):
        response = self.client.post(self.url_predict, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Flood risk data created successfully")
        self.assertIn('flood_risk', response.data)

    def test_create_flood_risk_missing_fields(self):
        data = self.valid_data.copy()
        del data['location']  # Remove location to test missing field
        response = self.client.post(self.url_predict, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Missing fields", response.data['error'])

    def test_create_flood_risk_invalid_risk_percentage(self):
        data = self.valid_data.copy()
        data['risk_percentage'] = "invalid_data"  # Invalid risk percentage
        response = self.client.post(self.url_predict, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Risk percentage must be a valid JSON object.", response.data['error'])

    def test_retrieve_flood_risk(self):
        # Create a flood risk entry first
        self.client.post(self.url_predict, self.valid_data, format='json')
        response = self.client.get(self.url_retrieve, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], self.valid_data['location'])

    def test_retrieve_non_existing_flood_risk(self):
        response = self.client.get(reverse('flood-risk', args=["Non Existing Location"]), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Location not found", response.data['error'])

    def test_update_flood_risk(self):
        # Create initial flood risk entry
        self.client.post(self.url_predict, self.valid_data, format='json')
        
        # Update the flood risk
        updated_data = self.valid_data.copy()
        updated_data['risk_percentage']['short_rains'] = 50  # Change the value
        response = self.client.post(self.url_predict, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Flood risk data updated successfully")
        
        # Retrieve and check the updated values
        response = self.client.get(self.url_retrieve, format='json')
        self.assertEqual(response.data['risk_percentage']['short_rains'], 50)

    def test_delete_flood_risk(self):
        # Create flood risk entry
        self.client.post(self.url_predict, self.valid_data, format='json')
        
        # Delete the flood risk
        response = self.client.delete(reverse('flood-risk', args=[self.valid_data['location']]), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Attempt to retrieve the deleted entry
        response = self.client.get(self.url_retrieve, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_risk_category(self):
        seasonal_thresholds = {
            "short_rains": [
                {"max": 25, "category": "low", "message": "Low risk during short rains."},
                {"max": 50, "category": "moderate", "message": "Moderate risk during short rains."},
                {"max": 100, "category": "high", "message": "High risk during short rains."}
            ]
        }
        risk_percentage = 30
        category = next(threshold for threshold in seasonal_thresholds["short_rains"] if risk_percentage <= threshold["max"])
        self.assertEqual(category['category'], 'moderate')

