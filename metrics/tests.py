from django.test import TestCase, Client 
from django.urls import reverse
from metrics.models import LocationSearch, Download
import json

class SearchLocationTestCase(TestCase):
    def setUp(self):
        self.client = Client()  

    def test_search_location_success(self):
        response = self.client.post(reverse('search_location'), data={'location': 'Nairobi'})
        self.assertEqual(response.status_code, 200)

    def test_search_location_fail(self):
        response = self.client.post(reverse('search_location'), data={'location': 'Unknown'})
        self.assertEqual(response.status_code, 404)

class DownloadReportTestCase(TestCase):
    def setUp(self):
        self.client = Client()  
        self.search_record = LocationSearch.objects.create(location='Nairobi', is_successful=True)

    def test_download_report_success(self):
        response = self.client.post(reverse('download_report'), data={'search_id': self.search_record.id})
        self.assertEqual(response.status_code, 200)

    def test_download_report_fail(self):
        response = self.client.post(reverse('download_report'), data={'search_id': 9999})
        self.assertEqual(response.status_code, 404)

class StatisticsTestCase(TestCase):
    def setUp(self):
        self.client = Client()  
        LocationSearch.objects.create(location='Nairobi', is_successful=True)
        LocationSearch.objects.create(location='Langata', is_successful=True)
        LocationSearch.objects.create(location='Dandora', is_successful=False)
        search = LocationSearch.objects.get(location='Nairobi')
        Download.objects.create(location_search=search)

    def test_statistics(self):
        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)
