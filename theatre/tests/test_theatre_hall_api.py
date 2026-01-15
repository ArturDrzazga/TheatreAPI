from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from theatre.models import TheatreHall


class TheatreHallApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="adminpassword"
        )
        self.hall = TheatreHall.objects.create(
            name="Blue Room",
            rows=10,
            seats_in_row=15
        )
        self.url = reverse("theatre:theatrehall-list")

    def test_list_theatre_halls(self):
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Blue Room")

    def test_retrieve_theatre_hall_detail(self):
        url = reverse("theatre:theatrehall-detail", args=[self.hall.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["capacity"], 150)
        self.assertEqual(res.data["name"], "Blue Room")

    def test_create_theatre_hall_forbidden_for_user(self):
        self.client.force_authenticate(self.user)
        payload = {
            "name": "New VIP Hall",
            "rows": 5,
            "seats_in_row": 5
        }
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_theatre_hall_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        payload = {
            "name": "Green Hall",
            "rows": 20,
            "seats_in_row": 20
        }
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TheatreHall.objects.count(), 2)
