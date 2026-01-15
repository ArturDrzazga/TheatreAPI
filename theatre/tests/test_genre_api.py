from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from theatre.models import Genre


class GenreApiTests(APITestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpassword"
        )
        self.genre = Genre.objects.create(name="Drama")
        self.url = reverse("theatre:genre-list")

    def test_list_genres(self):
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Drama")

    def test_create_genre_forbidden_for_user(self):
        self.client.force_authenticate(self.user)
        payload = {"name": "Comedy"}
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_genre_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        payload = {"name": "Science-Fiction"}
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_create_genre_duplicate_validation(self):
        self.client.force_authenticate(self.admin)
        payload = {"name": "drama"}
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", res.data["name"][0])