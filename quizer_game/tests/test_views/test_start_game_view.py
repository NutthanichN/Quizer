from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player


def create_player(quiz, player_name) -> Player:
    """
    Create a player of the given `quiz` and set player statuses to playing state
    """
    player = quiz.player_set.create(name=player_name)
    player.current_question = quiz.question_set.get(id=1)
    player.is_playing = True
    player.save()
    return player


class StartGameTest(TestCase):
    def setUp(self) -> None:
        """
        Setup quiz and player
        """
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)
        self.choice1 = Choice.objects.create(question=self.question, text='String', value=1)
        self.choice2 = Choice.objects.create(question=self.question, text="I don't know", value=0)

        # # setup player
        # self.player = create_player(self.quiz, 'Player1')
        #
        # # setup player's timer
        # self.timer = self.player.timer_set.create()
        # self.timer.start()

    def test_can_access_by_url_name(self):
        """
        Test that a view can be access using url name
        """
        url = reverse('quizer_game:start-game', args=('Player1', ))
        response = self.client.post(url, data={'quiz_id': self.quiz.id,
                                               'difficulty': 'easy'})
        self.assertEqual(response.status_code, 302)

    # def test_redirect_to_game_view(self):
    #     url = reverse('quizer_game:start-game', args=('Player1',))
    #     response = self.client.post(url, data={'quiz_id': self.quiz.id,
    #                                            'difficulty': 'easy'})
    #     url_redirect = reverse('quizer_game:game',
    #                            kwargs={'player_id': player.id,
    #                                    'quiz_id': self.quiz.id,
    #                                    'selected_difficulty': player.selected_difficulty,
    #                                    }
    #                            )
    #     self.assertRedirects(response, url_redirect)

    def test_can_create_new_player(self):
        """
        Create a new player when start a game
        """
        total_player_old = len(self.quiz.player_set.all())
        url = reverse('quizer_game:start-game', args=('Player1', ))
        self.client.post(url, data={'quiz_id': self.quiz.id,
                                    'difficulty': 'easy'})
        total_player_new = len(self.quiz.player_set.all())
        self.assertEqual(total_player_new, total_player_old + 1)
