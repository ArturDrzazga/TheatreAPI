from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from theatre.models import (
    Reservation,
    Performance,
    Play,
    TheatreHall,
    Ticket
)


class ReservationApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.other_user = get_user_model().objects.create_user(
            email="other@test.com",
            password="password123"
        )
        self.hall = TheatreHall.objects.create(
            name="Main",
            rows=10,
            seats_in_row=10
        )
        self.play = Play.objects.create(
            title="Test Play",
            description="Desc"
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timezone.timedelta(days=1)
        )

        self.url = reverse("theatre:reservation-list")

    def test_list_reservations_is_private(self):
        res_user = Reservation.objects.create(user=self.user)
        Reservation.objects.create(user=self.other_user)

        self.client.force_authenticate(self.user)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_reservation(self):
        self.client.force_authenticate(self.user)

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "performance": self.performance.id  # Musi tu być!
                }
            ]
        }

        res = self.client.post(self.url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_unauthorized(self):
        payload = {
            "tickets": [{"row": 1, "seat": 1, "performance": self.performance.id}]
        }
        res = self.client.post(self.url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
