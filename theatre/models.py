from django.db.models.functions import Lower
from django.utils import timezone

from django.core.validators import MinValueValidator
from django.db import models

from django.conf import settings
from rest_framework.exceptions import ValidationError


class Actor(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="genre_name_unique_lower",
            )
        ]

    def __str__(self):
        return f"{self.name}"


class Play(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(null=True, blank=True, upload_to="uploads/")

    def __str__(self):
        return f"{self.title} : {self.description}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    seats_in_row = models.IntegerField(
        validators=[MinValueValidator(1)],
    )

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


    def __str__(self):
        return f"{self.name} with {self.capacity} seats"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="reservations")


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["theatre_hall", "show_time"],
                name="unique_performance_hall_time"
            ),
            models.UniqueConstraint(
                fields=["play", "show_time"],
                name="unique_performance_play_time"
            )
        ]

    def clean(self):
        if self.show_time < timezone.now():
            raise ValidationError("Show time cannot be in the past")

    def __str__(self):
        return f"{self.play.title} in {self.theatre_hall.name} at {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row","seat","performance"],
                name="unique_ticket_seat_performance"
            )
        ]
        ordering = ["row", "seat"]

    @property
    def row_seat_display(self):
        return f"Row: {self.row} Seat: {self.seat}"

    @staticmethod
    def validate_ticket(seat: int, row:int, theatre_hall: TheatreHall):
        if not (1 <= seat <= theatre_hall.seats_in_row):
            raise ValidationError(f"Seat must be in range between 1 and {theatre_hall.seats_in_row}")
        if not (1 <= row <= theatre_hall.rows):
            raise ValidationError(f"Row must be in range between 1 and {theatre_hall.rows}")

    def clean(self):
        Ticket.validate_ticket(self.seat, self.row, self.performance.theatre_hall)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


    def __str__(self):
        return (f"{self.performance.play.title} in "
                f"{self.performance.theatre_hall.id} at "
                f"{self.performance.show_time} row: {self.row} seat: {self.seat}")
