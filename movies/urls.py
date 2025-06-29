from django.urls import path
from .views import (
    MovieListCreateView,
    MovieDetailView,
    top_genres_view,
    recent_hits_view,
    count_by_year_view,
    avg_rating_by_genre_view,
    movie_form_view,  # classic form interface
)

urlpatterns = [
    # Core CRUD endpoints
    path(
        'movies/', 
        MovieListCreateView.as_view(), 
        name='movie-list-create'
    ),  # GET all / POST new
    path(
        'movies/<int:pk>/', 
        MovieDetailView.as_view(), 
        name='movie-detail'
    ),  # GET/PUT/DELETE single movie

    # Analytics endpoints
    path(
        'movies/top_genres/', 
        top_genres_view, 
        name='top-genres'
    ),  # genre counts across dataset
    path(
        'movies/count_by_year/', 
        count_by_year_view, 
        name='count-by-year'
    ),  # number of movies per year
    path(
        'movies/recent_hits/', 
        recent_hits_view, 
        name='recent-hits'
    ),  # recent movies with rating ≥ 8
    path(
        'movies/avg_rating_by_genre/', 
        avg_rating_by_genre_view, 
        name='avg-rating-by-genre'
    ),  # average score per genre

    # Traditional Django form
    path(
        'movies/add/', 
        movie_form_view, 
        name='movie-form'
    ),  # HTML form to add a movie
]
