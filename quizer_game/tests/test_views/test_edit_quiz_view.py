from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quizer_game.models import Quiz, Question, Choice, Player


class EditQuizTest(TestCase):

    def setUp(self):
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Hello')

        #set up client
        self.client = Client()
        self.username = "Hello"
        self.password = "world"
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_can_view_edit_quiz(self):
        """Test that a user can view edit quiz"""

        self.client.force_login(self.user)
        url = reverse('quizer_game:edit_quiz', kwargs={'quiz_id': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/edit-question-set.html')

    def test_can_view_edit_quiz_player(self):
        """Test that a player can not view edit quiz"""

        url = reverse('quizer_game:edit_quiz', kwargs={'quiz_id': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/login_result.html')