from django.test import TestCase
from django.urls import reverse


class LeaderboardIndexTest(TestCase):
    def test_can_access_leaderboard_index_by_url_name(self):
        """
        Test that a leaderboard index page can be access using url name
        """
        url = reverse('quizer_game:leaderboard-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_index_uses_correct_template(self):
        """
        Test that a view renders `leaderboard-index.html`
        """
        url = reverse('quizer_game:leaderboard-index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quizer_game/leaderboard-index.html')
