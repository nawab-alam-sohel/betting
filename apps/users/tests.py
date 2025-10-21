from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User


class UserAPITestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.register_url = reverse('register')
		self.login_url = reverse('login')

	def test_register_and_login(self):
		# Register a new user
		resp = self.client.post(self.register_url, data={
			'email': 'test@example.com',
			'password': 'strongpassword',
			'name': 'Test User'
		})
		self.assertEqual(resp.status_code, 201)

		# Login with the new user
		resp = self.client.post(self.login_url, data={
			'email': 'test@example.com',
			'password': 'strongpassword'
		})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('access', data)
