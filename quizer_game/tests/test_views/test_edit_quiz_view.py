from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player



class EditQuizTest(TestCase):

    def setUp(self):
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Hello')

    def test_can_view_edit_quiz(self):
        """Test that a user can view edit quiz"""
        url = reverse('quizer_game:edit_quiz', kwargs={'quiz_id': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'quizer_game/edit-question-set.html')