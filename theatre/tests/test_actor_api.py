from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from theatre.models import Actor


class ActorApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpassword"
        )
        self.actor = Actor.objects.create(
            first_name="Tom",
            last_name="Clooney"
        )
        self.url = reverse("theatre:actor-list")

    def test_list_actors(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["first_name"], "Tom")

    def test_retrieve_actor_detail(self):
        url = reverse("theatre:actor-detail", args=[self.actor.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["full_name"], "Tom Clooney")
        self.assertNotIn("first_name", res.data)

    def test_create_actor_forbidden_for_user(self):
        self.client.force_authenticate(self.user)
        payload = {"first_name": "Brad", "last_name": "Pitt"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_actor_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        payload = {"first_name": "Brad", "last_name": "Pitt"}
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
