from django.test import TestCase
from django.urls import reverse


class QuizLevelTest(TestCase):
    def test_can_access_by_url_name(self):
        """
        Test that a view can be access using url name
        """
        url = reverse('quizer_game:quiz-level')
        response = self.client.post(url, data={'player_name': 'Player1'})
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that a view renders `question-level.html`
        """
        url = reverse('quizer_game:quiz-level')
        response = self.client.post(url, data={'player_name': 'Player1'})
        self.assertTemplateUsed(response, 'quizer_game/question-level.html')
