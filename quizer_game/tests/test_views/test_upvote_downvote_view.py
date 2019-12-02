from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz, Player


def create_player(quiz, player_name) -> Player:
    """
    Create a player of the given `quiz` and set player statuses to playing state
    """
    player = quiz.player_set.create(name=player_name)
    player.save()
    return player


class UpvoteDownvoteTest(TestCase):
    def setUp(self) -> None:
        """
        Setup quiz and player
        """
        # setup quiz
        self.quiz = Quiz.objects.create(topic='Python')

        # setup player
        self.player = self.quiz.player_set.create(name='Player1')
        self.player.has_vote = True
        self.player.save()

        self.upvote_code = 1
        self.downvote_code = 0

    def test_can_access_by_url_name(self):
        url = reverse('quizer_game:upvote-downvote',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty,
                              'code': self.upvote_code
                              }
                      )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_correct_view(self):
        """
        Test that upvote_downvote view redirect to result view
        """
        url = reverse('quizer_game:upvote-downvote',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty,
                              'code': self.upvote_code
                              }
                      )
        response = self.client.get(url)
        self.assertRedirects(response,
                             reverse('quizer_game:result',
                                     kwargs={'player_id': self.player.id,
                                             'quiz_id': self.quiz.id,
                                             'selected_difficulty': self.player.selected_difficulty
                                             }
                                     )
                             )

    def test_can_upvote(self):
        old_total_upvote = self.quiz.upvotes
        url = reverse('quizer_game:upvote-downvote',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty,
                              'code': self.upvote_code
                              }
                      )
        self.client.get(url)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.upvotes, old_total_upvote + 1)

    def test_can_downvote(self):
        old_total_downvote = self.quiz.downvotes
        url = reverse('quizer_game:upvote-downvote',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty,
                              'code': self.downvote_code
                              }
                      )
        self.client.get(url)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.downvotes, old_total_downvote + 1)

    def test_player_can_vote_once(self):
        """
        If player already voted, player.has_vote will be False
        """
        self.assertTrue(self.player.has_vote)
        url = reverse('quizer_game:upvote-downvote',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty,
                              'code': self.upvote_code
                              }
                      )
        self.client.get(url)
        self.player.refresh_from_db()
        self.assertFalse(self.player.has_vote)
