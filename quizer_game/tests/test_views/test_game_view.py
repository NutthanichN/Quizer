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


class GameTest(TestCase):
    def setUp(self) -> None:
        """
        Setup quiz and player
        """
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)
        self.choice1 = Choice.objects.create(question=self.question, text='String', value=1)
        self.choice2 = Choice.objects.create(question=self.question, text="I don't know", value=0)

        # setup player
        self.player = create_player(self.quiz, 'Player1')

        # setup player's timer
        self.timer = self.player.timer_set.create()
        self.timer.start()

    def test_can_access_by_url_name(self):
        """
        Test that a view can be access using url name
        """
        url = reverse('quizer_game:game', kwargs={'player_id': self.player.id, 'quiz_id': self.quiz.id,
                                                  'selected_difficulty': self.player.selected_difficulty})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that a view renders `game.html`
        """
        url = reverse('quizer_game:game', kwargs={'player_id': self.player.id, 'quiz_id': self.quiz.id,
                                                  'selected_difficulty': self.player.selected_difficulty})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quizer_game/game.html')

