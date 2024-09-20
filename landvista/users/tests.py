import json
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from .utils import send_email, generate_confirmation_link
from unittest.mock import patch
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user-registration')
    def test_user_registration_success(self):
        data = {
            'email': 'vivyndegwa@gmail.com',
            'password': 'TestPass123',
            'first_name': 'Mary',
            'last_name': 'Muthoni'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'vivyndegwa@gmail.com')
    def test_user_registration_invalid_data(self):
        data = {
            'email': 'invalid_email',
            'password': 'short',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, 400)
class UserDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Mary', email='vivyndegwa@gmail.com', password='testpass')
        self.detail_url = reverse('user-detail', args=[self.user.id])
    def test_get_user_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'vivyndegwa@gmail.com')
    def test_update_user_detail(self):
        data = {'first_name': 'Updated', 'last_name': 'Name'}
        response = self.client.put(self.detail_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
    def test_delete_user(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), 0)
class UtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='vivyndegwa@gmail.com', password='testpass')
        self.factory = RequestFactory()
    @patch('users.utils.EmailMessage.send')
    def test_send_email(self, mock_send):
        mock_send.return_value = True
        result = send_email('Test Subject', 'vivyndegwa@gmail.com', {'user': 'testuser'})
        self.assertTrue(result)
        self.assertEqual(mock_send.call_count, 1)
    def test_generate_confirmation_link(self):
        request = self.factory.get('/')
        link = generate_confirmation_link(self.user, request)
        self.assertIn('/confirm-registration/', link)
        parts = link.split('/confirm-registration/')[1].split('/')
        uidb64, token = parts[0], parts[1]
        self.assertTrue(uidb64)
        self.assertTrue(token)