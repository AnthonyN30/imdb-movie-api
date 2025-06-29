from django.db import models

class Movie(models.Model):
    # The movie’s title (e.g. "Avatar")
    title        = models.CharField(max_length=255)
    # Pipe-separated genres (e.g. "Action|Adventure")
    genres       = models.CharField(max_length=255)
    # Year of release stored as text; optional if unknown
    release_date = models.CharField(max_length=100, blank=True, null=True)
    # IMDb score (0.0–10.0); optional
    vote_average = models.FloatField(blank=True, null=True)
    # A short description or keywords; optional
    overview     = models.TextField(blank=True, null=True)

    def __str__(self):
        # When we print a Movie, show its title
        return self.title
