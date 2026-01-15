from django.test import TestCase

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from theatre.models import TheatreHall, Play, Actor, Genre, Performance, Reservation, Ticket


class ModelTests(TestCase):
    def setUp(self):
        self.theatre_hall = TheatreHall.objects.create(
            name="testhall",
            rows=10,
            seats_in_row=10
        )
        self.play = Play.objects.create(
            title="test",
            description="test"
        )
        self.user = get_user_model().objects.create_user(
            email="test@test3333.com",
            password="test123"
        )

    def test_actor_full_name(self):
        actor = Actor.objects.create(
            first_name="test",
            last_name="test",
        )
        return self.assertEqual(actor.full_name, "test test")

    def test_theatre_hall_capacity(self):
        return self.assertEqual(self.theatre_hall.capacity, 100)

    def test_genre_unique_constraint(self):
        Genre.objects.create(name="Drama")

        with self.assertRaises(Exception):
            Genre.objects.create(name="drama")

    def test_ticket_validation(self):
        performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time=timezone.now() + timezone.timedelta(days=1)
        )
        reservation = Reservation.objects.create(user=self.user)
        ticket = Ticket(row=10, seat=11, performance=performance, reservation=reservation)

        with self.assertRaises(ValidationError):
            ticket.full_clean()