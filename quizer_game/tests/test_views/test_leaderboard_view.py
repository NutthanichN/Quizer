from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Question, Choice, Player
from datetime import timedelta


def create_achieved_player(quiz: Quiz, player_name: str) -> Player:
    player = quiz.player_set.create(name=player_name)
    player.is_achieved = True
    player.save()
    return player


class LeaderboardTest(TestCase):
    def setUp(self) -> None:
        """
        Setup quiz and players for testing
        """
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Python')
        self.question = Question.objects.create(quiz=self.quiz, text='What is str?', number=1)
        self.choice1 = Choice.objects.create(question=self.question, text='String', value=1)
        self.choice2 = Choice.objects.create(question=self.question, text="I don't know", value=0)

        # setup player
        self.player1 = create_achieved_player(self.quiz, 'Player1')
        self.player2 = create_achieved_player(self.quiz, 'Player2')
        self.player3 = create_achieved_player(self.quiz, 'Player3')

    def test_can_access_leaderboard_by_url_name(self) -> None:
        """
        Test that a leaderboard page can be access using url name
        """
        url = reverse('quizer_game:leaderboard',
                      kwargs={'quiz_id': self.quiz.id,
                              'selected_difficulty': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_uses_correct_template(self) -> None:
        """
        Test that a view renders `leaderboard.html`
        """
        url = reverse('quizer_game:leaderboard',
                      kwargs={'quiz_id': self.quiz.id,
                              'selected_difficulty': 0})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quizer_game/leaderboard.html')

    # def test_leaderboard_ranks_players_using_time_in_ascending_order(self) -> None:
    #     """
    #     Test that players are ranked in ascending order
    #     """
    #     self.player1.time = timedelta(minutes=5)
    #     self.player1.save()
    #
    #     self.player2.time = timedelta(seconds=59)
    #     self.player2.save()
    #
    #     self.player3.time = timedelta(seconds=58)
    #     self.player3.save()
    #
    #     url = reverse('quizer_game:leaderboard',
    #                   kwargs={'quiz_id': self.quiz.id,
    #                           'selected_difficulty': 0})
    #     response = self.client.get(url)
    #     player_list = list(response.context['players'])
    #     self.assertQuerysetEqual(player_list, ['<Player: Player3>', '<Player: Player2>', '<Player: Player1>'])

    def test_leaderboard_displays_achieved_player(self) -> None:
        """
        Leaderboard only displays players who reach the finish line (achieved)
        """
        self.player2.is_achieved = False
        self.player2.save()

        url = reverse('quizer_game:leaderboard',
                      kwargs={'quiz_id': self.quiz.id,
                              'selected_difficulty': 0})
        response = self.client.get(url)
        player_list = list(response.context['players'])
        self.assertQuerysetEqual(player_list, ['<Player: Player1>', '<Player: Player3>'])

    def test_leaderboard_displays_players_who_play_the_same_difficulty(self) -> None:
        """
        Leaderboard of each quiz and each difficulty displays players in the same difficulty
        """
        self.player1.selected_difficulty = 0
        self.player1.save()

        self.player2.selected_difficulty = 1
        self.player2.save()

        self.player3.selected_difficulty = 1
        self.player3.save()

        url = reverse('quizer_game:leaderboard',
                      kwargs={'quiz_id': self.quiz.id,
                              'selected_difficulty': 1})
        response = self.client.get(url)
        player_list = list(response.context['players'])
        self.assertQuerysetEqual(player_list, ['<Player: Player2>', '<Player: Player3>'])
