import pytz
from rest_framework import serializers

from moviebase.settings import TIME_ZONE
from movielist.models import Movie
from showtimes.models import Cinema, Screening


TZ = pytz.timezone(TIME_ZONE)


class CinemaSerializer(serializers.ModelSerializer):
    movies = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movies-detail'
    )

    class Meta:
        model = Cinema
        fields = ['name', 'city', 'movies']


class ScreeningSerializer(serializers.ModelSerializer):
    cinema = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Cinema.objects.all()
    )
    movie = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Movie.objects.all()
    )

    class Meta:
        model = Screening
        fields = ['movie', 'cinema', 'date']
