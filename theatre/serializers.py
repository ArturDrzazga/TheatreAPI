from rest_framework import serializers

from theatre.models import Actor, Genre, Play, TheatreHall


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