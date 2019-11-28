from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player


class GameTest(TestCase):
    def setUp(self):
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)
        self.choice1 = Choice.objects.create(question=self.question, text='String', value=1)
        self.choice2 = Choice.objects.create(question=self.question, text="I don't know", value=0)

        # setup player
        self.player = self.quiz.player_set.create(name='player1')
        self.player.current_question = self.question
        self.player.is_playing = True
        self.player.save()

    def test_can_view_game(self):
        """Test that a player can view game"""
        url = reverse('quizer_game:game', kwargs={'player_id': self.player.id, 'quiz_id': self.quiz.id,
                                                  'selected_difficulty': self.player.selected_difficulty})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/game.html')


class SystemTest(TestCase):
    def test_can_view_index(self):
        """ Test that anyone can see index page """
        url = reverse('quizer_game:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/index.html')

    def test_can_view_leaderboard_index(self):
        """ Test that anyone can see leaderboard index """
        url = reverse('quizer_game:leaderboard-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/leaderboard-index.html')

    def test_can_view_login(self):
        """ Test that anyone can see login page """
        url = reverse('quizer_game:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/login.html')

    def test_can_view_leaderboard(self):
        """ Test that anyone can see leaderboard """
        url = reverse('quizer_game:leaderboard', kwargs={'quiz_id': self.quiz.id,
                                                         'selected_difficulty': self.player.selected_difficulty})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/leaderboard.html')

