from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player


class ResultTest(TestCase):
    def setUp(self) -> None:
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)

        self.player = self.quiz.player_set.create(name='Player1', current_question=self.question)

    def test_can_access_by_url_name(self) -> None:
        """
        Test that result view can be accessed by url name
        """
        url = reverse('quizer_game:result',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_result_uses_correct_template(self) -> None:
        """
        Test that result view renders result.html
        """
        player1 = self.quiz.player_set.get(id=1)
        url = reverse('quizer_game:result',
                      kwargs={'player_id': player1.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quizer_game/result.html')
