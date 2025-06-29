from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer

import sys, django  # to get Python and Django version info for the homepage
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .forms import MovieForm

# ---- API Endpoints ----

class MovieListCreateView(generics.ListCreateAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        # Start with all Movie records, then apply filters based on URL params
        qs = Movie.objects.all()
        title    = self.request.query_params.get('title')           # filter by title substring
        genres   = self.request.query_params.get('genres')          # filter by genre substring
        year     = self.request.query_params.get('release_date')    # filter by exact release year
        min_vote = self.request.query_params.get('vote_average__gte')  # filter by minimum rating

        if title:
            qs = qs.filter(title__icontains=title)      # case-insensitive title match
        if genres:
            qs = qs.filter(genres__icontains=genres)    # any genre containing the substring
        if year:
            qs = qs.filter(release_date=year)           # exact year match
        if min_vote:
            qs = qs.filter(vote_average__gte=float(min_vote))  # numeric comparison

        return qs


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: retrieve a single movie by ID
    PUT: update an existing movie
    DELETE: remove a movie from the database
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# ---- Landing Page ----

def api_home_view(request):
    """
    Render the homepage with version info, package list, admin credentials, and endpoint links.
    """
    ctx = {
        'python_version': sys.version.split()[0],  # e.g. '3.12.4'
        'django_version': django.get_version(),    # e.g. '5.2.3'
        'packages': [  # key libraries used in this project
            f"Django {django.get_version()}",
            "djangorestframework 3.x",
        ],
        'admin_username': 'admin',        # superuser credentials for graders
        'admin_password': 'Password123',
    }
    return render(request, 'movies/index.html', ctx)


# ---- Custom API Views ----

@api_view(['GET'])
def top_genres_view(request):
    """
    Return a sorted list of genres by how many movies belong to each.
    """
    counts = {}
    # Build a count for each genre in the dataset
    for movie in Movie.objects.all():
        if movie.genres:
            for g in movie.genres.split('|'):
                counts[g] = counts.get(g, 0) + 1
    # Sort genres descending by their count
    sorted_list = sorted(counts.items(), key=lambda i: i[1], reverse=True)
    # Format as JSON list of {'genre': name, 'count': number}
    return Response([{'genre': g, 'count': c} for g, c in sorted_list])


@api_view(['GET'])
def recent_hits_view(request):
    current = timezone.now().year
    # read ?years= from URL, default 5 Movies from last 10 years with rating ≥ 8 (use `?years=N` to change window)
    years = int(request.query_params.get('years', 10))
    cutoff = str(current - years)
    hits = Movie.objects.filter(
        release_date__gte=cutoff,
        vote_average__gte=8.0
    )
    return Response(MovieSerializer(hits, many=True).data)



@api_view(['GET'])
def count_by_year_view(request):
    """
    Return each release year and the number of movies from that year.
    """
    counts = {}
    # Tally movies by their release_date field
    for m in Movie.objects.all():
        year = m.release_date
        if year:
            counts[year] = counts.get(year, 0) + 1
    # Sort by movie count descending
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return Response([{'year': y, 'count': c} for y, c in sorted_counts])


@api_view(['GET'])
def avg_rating_by_genre_view(request):
    """
    Calculate and return average vote_average for each genre.
    """
    totals, counts = {}, {}
    # Sum up total ratings and count for each genre
    for m in Movie.objects.all():
        if m.genres:
            for g in m.genres.split('|'):
                totals[g] = totals.get(g, 0.0) + (m.vote_average or 0)
                counts[g] = counts.get(g, 0) + (1 if m.vote_average is not None else 0)
    # Compute the average, round to 2 decimals, and sort
    avgs = [
        {'genre': g, 'avg_rating': round(totals[g] / counts[g], 2)}
        for g in totals if counts[g] > 0
    ]
    avgs.sort(key=lambda x: x['avg_rating'], reverse=True)
    return Response(avgs)


# ---- Classic Django Form View ----

def movie_form_view(request):
    """
    Render an HTML form for creating movies with custom validation logic.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():  # uses clean_release_date and clean_genres
            form.save()
            return redirect('api-home')  # go back to homepage on success
    else:
        form = MovieForm()  # empty form for GET requests
    # Render the form template, passing in the form object
    return render(request, 'movies/movie_form.html', {'form': form})
