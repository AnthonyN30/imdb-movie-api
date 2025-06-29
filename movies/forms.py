from django import forms
from django.utils import timezone
from .models import Movie

# Allowed genres for the dropdown (pipe-separated in the form)
ALLOWED_GENRES = {
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
    'Film-Noir', 'History', 'Horror', 'Music', 'Mystery',
    'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller',
    'War', 'Western', 'News'
}

class MovieForm(forms.ModelForm):
    """
    Form for creating/updating Movie objects with extra validation.
    """
    class Meta:
        model = Movie
        fields = ['title', 'genres', 'release_date', 'vote_average', 'overview']
        widgets = {
            # Make overview a small textarea
            'overview': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def clean_release_date(self):
        data = self.cleaned_data['release_date']
        # Must be exactly four digits
        if not (data.isdigit() and len(data) == 4):
            raise forms.ValidationError("Enter a four-digit year, e.g. 2023.")
        year = int(data)
        current_year = timezone.now().year
        # Limit to realistic movie years
        if year < 1900 or year > current_year:
            raise forms.ValidationError(f"Year must be between 1900 and {current_year}.")
        return data

    def clean_genres(self):
        data = self.cleaned_data['genres']
        invalid = []
        # Split on '|' and check each against our allowed list
        for g in data.split('|'):
            if g not in ALLOWED_GENRES:
                invalid.append(g)
        if invalid:
            allowed_list = ', '.join(sorted(ALLOWED_GENRES))
            raise forms.ValidationError(
                f"Invalid genre(s): {', '.join(invalid)}. "
                f"Choose from: {allowed_list}."
            )
        return data
