import csv, os
from movies.models import Movie

# Path to the downloaded CSV dataset
CSV_PATH = os.path.join(os.path.dirname(__file__), 'movie_metadata.csv')

def load_movies():
    """Read each row from the CSV and save it as a Movie."""
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a Movie for every CSV row
            Movie.objects.create(
                title        = row['movie_title'].strip(),
                genres       = row['genres'], # e.g. "Action|Drama"
                release_date = row['title_year'], # e.g. "2012"
                vote_average = row['imdb_score'], # e.g. "7.8"
                overview     = row['plot_keywords'] # keyword list
            )
    print(" Movie data loaded successfully.")
