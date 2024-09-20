from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch, Mock
from .models import Location

class SearchViewTests(APITestCase):

    @patch('location.views.requests.get')
    def test_search_new_location(self, mock_get):
        # Mock the geocoding API response
        mock_get.side_effect = [
            # Geocoding response
            Mock(status_code=200, json=lambda: {
                'status': 'OK',
                'results': [{
                    'geometry': {
                        'location': {
                            'lat': 40.7128,
                            'lng': -74.0060
                        }
                    }
                }]
            }),
            # Mock soil type response
            Mock(status_code=200, json=lambda: {'soil_type': 'Loamy'}),
            # Mock elevation response
            Mock(status_code=200, json=lambda: {
                'results': [{'elevation': 10}]
            })
        ]

        response = self.client.post(reverse('search'), {'location': 'New York'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('soil_type', response.data)
        self.assertIn('elevation', response.data)

    # Additional test methods...
