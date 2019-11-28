from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player


class CreateQuizTest(TestCase):
    def test_can_view_create_quiz(self):
        """Test that a user can view create quiz"""
        url = reverse('quizer_game:create-question-set')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'quizer_game/create-question.html')


