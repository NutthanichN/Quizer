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

        # setup player's timer
        self.timer = self.player.timer_set.create()
        self.timer.start()

    def test_can_view_game(self):
        """Test that a player can view game"""
        url = reverse('quizer_game:game', kwargs={'player_id': self.player.id, 'quiz_id': self.quiz.id,
                                                  'selected_difficulty': self.player.selected_difficulty})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/game.html')