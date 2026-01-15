from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from theatre.models import Performance, Play, TheatreHall, Reservation, Ticket


class PerformanceApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpassword"
        )

        self.hall = TheatreHall.objects.create(
            name="Main",
            rows=5,
            seats_in_row=5
        )
        self.play = Play.objects.create(
            title="Hamlet",
            description="Shakespeare"
        )

        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now()
        )

        self.url = reverse("theatre:performance-list")

    def test_list_performances_with_available_seats(self):
        reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=reservation
        )

        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]["available_seats"], 24)

    def test_filter_performances_by_play(self):
        other_play = Play.objects.create(title="Other Movie", description="Desc")
        Performance.objects.create(
            play=other_play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timezone.timedelta(hours=2)
        )

        res = self.client.get(self.url, {"play": self.play.id})

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Hamlet")

    def test_filter_performances_by_date(self):
        future_date = timezone.now() + timezone.timedelta(days=5)
        Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=future_date
        )

        date_str = future_date.strftime("%Y-%m-%d")
        res = self.client.get(self.url, {"date": date_str})

        self.assertEqual(len(res.data), 1)

    def test_create_performance_admin_required(self):
        self.client.force_authenticate(self.user)
        payload = {
            "play": self.play.id,
            "theatre_hall": self.hall.id,
            "show_time": timezone.now()
        }
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
