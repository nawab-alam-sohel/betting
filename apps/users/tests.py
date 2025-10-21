from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from rest_framework.test import APIClient
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserAPITestCase(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		self.profile_url = reverse('profile')
		self.logout_url = reverse('logout')
		self.change_password_url = reverse('change-password')
		self.reset_password_url = reverse('password_reset')

		self.user_data = {
			'email': 'test@example.com',
			'password': 'strongpassword',
			'name': 'Test User'
		}

	def create_user_and_get_tokens(self):
		# register
		self.client.post(self.register_url, data=self.user_data)
		# login
		resp = self.client.post(self.login_url, data={'email': self.user_data['email'], 'password': self.user_data['password']})
		tokens = resp.json()
		return tokens

	def test_register_and_login(self):
		tokens = self.create_user_and_get_tokens()
		self.assertIn('access', tokens)

	def test_profile_requires_auth(self):
		tokens = self.create_user_and_get_tokens()
		access = tokens['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.get(self.profile_url)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json().get('email'), self.user_data['email'])

	def test_logout_blacklists_refresh(self):
		tokens = self.create_user_and_get_tokens()
		refresh = tokens['refresh']
		access = tokens['access']
		# set auth header so logout view (IsAuthenticated) accepts the request
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.post(self.logout_url, data={'refresh': refresh})
		self.assertEqual(resp.status_code, 205)

	def test_change_password(self):
		tokens = self.create_user_and_get_tokens()
		access = tokens['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp = self.client.put(self.change_password_url, data={'old_password': self.user_data['password'], 'new_password': 'newstrongpassword'})
		self.assertEqual(resp.status_code, 200)

	def test_reset_password_flow(self):
		# create user
		user = User.objects.create(email='reset@example.com')
		user.set_password('oldpass')
		user.save()

		token = PasswordResetTokenGenerator().make_token(user)
		uid = urlsafe_base64_encode(force_bytes(user.id))

		resp = self.client.post(self.reset_password_url, data={'password': 'newpass123', 'confirm_password': 'newpass123', 'uidb64': uid, 'token': token})
		# expecting 200 on success
		self.assertEqual(resp.status_code, 200)
