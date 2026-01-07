from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import Actor, Genre, Play, TheatreHall, Performance
from theatre.serializers import ActorSerializer, GenreSerializer, ActorRetrieveSerializer, PlaySerializer, \
    PlayRetrieveSerializer, TheatreHallRetrieveSerializer, TheatreHallSerializer, PerformanceSerializer, \
    PerformanceRetrieveSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ActorRetrieveSerializer
        return ActorSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PlayRetrieveSerializer
        return PlaySerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheatreHallRetrieveSerializer
        return TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerformanceRetrieveSerializer
        return PerformanceSerializer
