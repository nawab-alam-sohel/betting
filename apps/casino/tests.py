from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.casino.models import CasinoProvider, CasinoCategory, CasinoGame


class CasinoAPITests(APITestCase):
    def setUp(self):
        # Seed minimal data
        self.provider = CasinoProvider.objects.create(key="generic", name="Generic Provider")
        self.cat_slots = CasinoCategory.objects.create(name="Slots", slug="slots")
        self.game = CasinoGame.objects.create(
            provider=self.provider,
            name="Alpha Slots",
            slug="alpha-slots",
            provider_game_id="GEN-1",
            active=True,
        )
        self.game.categories.add(self.cat_slots)
        self.client = APIClient()

    def test_list_providers(self):
        url = "/api/casino/providers/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(p["key"] == "generic" for p in resp.json()))

    def test_list_categories(self):
        url = "/api/casino/categories/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        slugs = [c["slug"] for c in resp.json()]
        self.assertIn("slots", slugs)

    def test_list_games_with_letter_filter(self):
        url = "/api/casino/games/?letter=A"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        names = [g["name"] for g in resp.json()]
        self.assertIn("Alpha Slots", names)

    def test_launch_requires_auth(self):
        url = "/api/casino/launch/"
        resp = self.client.post(url, {"game_id": self.game.id}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_launch_game_authenticated(self):
        user = get_user_model().objects.create_user(email="u1@example.com", password="pass12345")
        self.client.force_authenticate(user=user)
        url = "/api/casino/launch/"
        resp = self.client.post(url, {"game_id": self.game.id}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertIn("launch_url", data)
        self.assertTrue(str(self.game.slug) in data["launch_url"]) 
