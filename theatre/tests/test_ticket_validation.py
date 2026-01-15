from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.test import TestCase
from theatre.models import Performance, Play, TheatreHall, Reservation, Ticket

class TicketValidationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@t.com",
            password="userpassword",
        )
        self.hall = TheatreHall.objects.create(name="Small Room", rows=3, seats_in_row=3)
        self.play = Play.objects.create(title="Test Play", description="Desc")
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2026-01-01T12:00:00Z"
        )
        self.reservation = Reservation.objects.create(user=self.user)

    def test_ticket_row_out_of_range(self):
        ticket = Ticket(
            row=4,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_ticket_seat_out_of_range(self):
        ticket = Ticket(
            row=1,
            seat=5,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(ValidationError):
            ticket.full_clean()

    def test_unique_together_ticket_validation(self):
        Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        duplicate_ticket = Ticket(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )
        with self.assertRaises(DjangoValidationError):
            duplicate_ticket.full_clean()
