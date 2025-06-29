from rest_framework.test import APITestCase
from django.urls import reverse
from movies.models import Movie

class MovieAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Seed a couple of movies for testing
        Movie.objects.create(
            title="Test A", genres="Drama",
            release_date="2020", vote_average=7.0, overview="A"
        )
        Movie.objects.create(
            title="Test B", genres="Action",
            release_date="2021", vote_average=8.5, overview="B"
        )

    def test_list_movies(self):
        """List endpoint returns all movies"""
        url = reverse('movie-list-create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Two test movies should appear
        self.assertTrue(len(resp.data) >= 2)

    def test_filter_by_vote(self):
        """Filtering by vote_average__gte should only return high-scoring movies"""
        url = reverse('movie-list-create') + '?vote_average__gte=8.0'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        titles = [m['title'] for m in resp.data]
        # Only the movie with score >= 8.0 should be present
        self.assertIn("Test B", titles)
        self.assertNotIn("Test A", titles)

    def test_get_detail(self):
        """Detail endpoint returns the correct movie by ID"""
        url  = reverse('movie-detail', args=[1])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], "Test A")

    def test_create_movie(self):
        """POST to create endpoint should add a new movie"""
        url  = reverse('movie-list-create')
        data = {
            "title": "Test C", "genres": "Comedy",
            "release_date": "2022",
            "vote_average": 6.5, "overview": "C"
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        # Check that the movie count increased
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Movie.objects.last().title, "Test C")

    def test_update_movie(self):
        """PUT to detail endpoint should update the movie"""
        url = reverse('movie-detail', args=[1])
        data = {
            "title": "Test A+", "genres": "Drama",
            "release_date": "2020", "vote_average": 7.1,
            "overview": "A+"
        }
        resp = self.client.put(url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        # Title should reflect the update
        self.assertEqual(Movie.objects.get(pk=1).title, "Test A+")

    def test_delete_movie(self):
        """DELETE should remove the movie from the database"""
        url  = reverse('movie-detail', args=[2])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        # Movie with ID=2 should be gone
        self.assertFalse(Movie.objects.filter(pk=2).exists())

    # --- New tests for custom analytics endpoints ---

    def test_top_genres(self):
        """GET top_genres should return genres counts correctly"""
        url  = reverse('top-genres')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Build a dict of genre -> count from response
        data = {item['genre']: item['count'] for item in resp.data}
        # We expect exactly one 'Drama' and one 'Action'
        self.assertEqual(data.get('Drama'), 1)
        self.assertEqual(data.get('Action'), 1)

    def test_recent_hits(self):
        """GET recent_hits should return only movies in the last 5 years with rating >= 8"""
        url  = reverse('recent-hits')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        titles = [m['title'] for m in resp.data]
        # Only 'Test B' qualifies (2021, score 8.5)
        self.assertIn('Test B', titles)
        self.assertNotIn('Test A', titles)

    def test_count_by_year(self):
        """GET count_by_year should tally movies per release year"""
        url  = reverse('count-by-year')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Convert response list into a dict year->count
        data = {item['year']: item['count'] for item in resp.data}
        # Each test movie has a unique year
        self.assertEqual(data.get('2020'), 1)
        self.assertEqual(data.get('2021'), 1)

    def test_avg_rating_by_genre(self):
        """GET avg_rating_by_genre should calculate average scores per genre"""
        url  = reverse('avg-rating-by-genre')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # Convert to dict genre->avg_rating
        data = {item['genre']: item['avg_rating'] for item in resp.data}
        # We expect Action:8.5 and Drama:7.0
        self.assertEqual(data.get('Action'), 8.5)
        self.assertEqual(data.get('Drama'), 7.0)
