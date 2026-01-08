from django.db.models import Count, F
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from theatre.models import Actor, Genre, Play, TheatreHall, Performance, Reservation
from theatre.serializers import ActorSerializer, GenreSerializer, ActorRetrieveSerializer, PlaySerializer, \
    PlayRetrieveSerializer, TheatreHallRetrieveSerializer, TheatreHallSerializer, PerformanceSerializer, \
    PerformanceRetrieveSerializer, ReservationSerializer, ReservationRetrieveSerializer, PerformanceListSerializer


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        return False


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActorRetrieveSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlayRetrieveSerializer
        return PlaySerializer

    def get_queryset(self):
        queryset = self.queryset

        title_filter = self.request.query_params.get('title', None)
        genre_filter = self.request.query_params.get('genre', None)
        actor_filter = self.request.query_params.get('actor', None)

        if title_filter:
            queryset = queryset.filter(title__icontains=title_filter)

        if genre_filter:
            genre_ids = [int(genre)
                         for genre in genre_filter.split(',')
                         if genre.strip().isdigit()
                         ]
            queryset = queryset.filter(genres__in=genre_ids)

        if actor_filter:
            actor_ids = [int(actor)
                         for actor in actor_filter.split(',')
                         if actor.strip().isdigit()
                         ]
            queryset = queryset.filter(actors__in=actor_ids)

        return queryset.distinct()


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheatreHallRetrieveSerializer
        return TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerformanceRetrieveSerializer
        return PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset
        play_filter = self.request.query_params.get("play", None)
        date_filter = self.request.query_params.get("date", None)

        if self.action == "list":
            queryset = Performance.objects.annotate(
                available_tickets=(
                    F("theatre_hall__rows") * F("theatre_hall__seats_in_row") - Count("tickets")
                )
            )

        if play_filter:
            play_ids = [int(play)
                            for play in play_filter.split(",")
                            if play.strip().isdigit()
                            ]
            queryset = queryset.filter(play__id__in=play_ids)

        if date_filter:
            queryset = queryset.filter(show_time__date=date_filter)

        return queryset



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReservationRetrieveSerializer
        return ReservationSerializer