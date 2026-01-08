from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation, Ticket


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class ActorRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ["id", "full_name"]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["id", "name"]

    def validate_name(self, value):
        if Genre.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("This genre is already exists")
        return value


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]


class PlayRetrieveSerializer(PlaySerializer):
    actors = serializers.SlugRelatedField(many=True, read_only=True, slug_field="full_name")
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]


class TheatreHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row"]


class TheatreHallRetrieveSerializer(TheatreHallSerializer):

    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class PerformanceSerializer(serializers.ModelSerializer):
    available_seats = serializers.IntegerField(source="available_tickets", read_only=True)

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time", "available_seats"]


class PerformanceRetrieveSerializer(PerformanceSerializer):
    title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)
    sold_tickets = serializers.SlugRelatedField(many=True,
                                                read_only=True,
                                                slug_field="row_seat_display",
                                                source="tickets"
                                                )

    class Meta:
        model = Performance
        fields = ["id", "title", "theatre_hall_name", "show_time", "sold_tickets"]


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_ticket(
            attrs["seat"],
            attrs["row"],
            attrs["performance"].theatre_hall,
        )
        return data

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]


class TicketRetrieveSerializer(serializers.ModelSerializer):
    performance = PerformanceRetrieveSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        with transaction.atomic():
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                try:
                    Ticket.objects.create(reservation=reservation, **ticket_data)
                except Exception as e:
                    raise ValidationError(str(e))

        return reservation

    def update(self, instance, validated_data):
        tickets_data = validated_data.pop("tickets", None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if tickets_data is not None:
                instance.tickets.all().delete()

                for ticket_data in tickets_data:
                    try:
                        Ticket.objects.create(reservation=instance, **ticket_data)
                    except Exception as e:
                        raise ValidationError(str(e))
        return instance


class ReservationRetrieveSerializer(ReservationSerializer):
    tickets = TicketRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields =["id", "created_at", "tickets"]
