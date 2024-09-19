from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Location

class SearchViewTests(APITestCase):
    
    def setUp(self):
        self.url = reverse('search')
        Location.objects.create(name='Kibera', latitude=-1.311484, longitude=36.787948)
        Location.objects.create(name='Kitisuru', latitude=-1.218598, longitude=36.8016)

    def test_search_location_success(self):
        data = {'location': 'Kibera'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Kibera')

    def test_search_location_invalid(self):
        data = {'location': 'kibera'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Enter a valid location'})

    def test_search_location_not_found(self):
        data = {'location': 'Unknown Place'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Location not found'})

    def test_search_location_already_exists(self):
        data = {'location': 'Kitisuru'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Kitisuru')
        self.assertEqual(Location.objects.count(), 2)  
