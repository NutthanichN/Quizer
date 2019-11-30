from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question


class QuitGameTest(TestCase):
    def setUp(self) -> None:
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)

        self.quiz.player_set.create(name='Player1', current_question=self.question)
        self.quiz.player_set.create(name='Player2', current_question=self.question)
        self.quiz.player_set.create(name='Player3', current_question=self.question)

    def test_can_access_by_url_name(self) -> None:
        """
        Test that quiz_index view can be accessed by url name
        """
        player1 = self.quiz.player_set.get(id=1)
        url = reverse('quizer_game:quit-game',
                      kwargs={'player_id': player1.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': player1.selected_difficulty
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_index_view(self) -> None:
        """
        Test that quit_game redirects to index page
        """
        player1 = self.quiz.player_set.get(id=1)
        url = reverse('quizer_game:quit-game',
                      kwargs={'player_id': player1.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': player1.selected_difficulty
                              }
                      )
        response = self.client.get(url)
        self.assertRedirects(response, reverse('quizer_game:index'))

    def test_delete_player(self) -> None:
        """
        Delete player when the player quit a game while a game doesn't end
        """
        old_num_player = len(self.quiz.player_set.all())
        player1 = self.quiz.player_set.get(id=1)
        url = reverse('quizer_game:quit-game',
                      kwargs={'player_id': player1.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': player1.selected_difficulty
                              }
                      )
        self.client.get(url)
        new_num_player = len(self.quiz.player_set.all())

        self.assertEqual(new_num_player, old_num_player - 1)
        self.assertQuerysetEqual(list(self.quiz.player_set.all()),
                                 ['<Player: Player2>', '<Player: Player3>']
                                 )
