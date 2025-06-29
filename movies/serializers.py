from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # Expose these fields in JSON API
        fields = ['id', 'title', 'genres', 'release_date', 'vote_average', 'overview']
