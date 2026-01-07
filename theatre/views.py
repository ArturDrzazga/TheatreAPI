from django.shortcuts import render
from rest_framework import viewsets

from theatre.models import Actor, Genre, Play
from theatre.serializers import ActorSerializer, GenreSerializer, ActorRetrieveSerializer, PlaySerializer, \
    PlayRetrieveSerializer


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