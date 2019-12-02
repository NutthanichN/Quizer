from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz
from datetime import timedelta


class UpdateGameTest(TestCase):
    def setUp(self) -> None:
        self.quiz = Quiz.objects.create(topic='Python')

        self.question1 = self.quiz.question_set.create(text='Question 1', number=1)
        self.correct_choice1 = self.question1.choice_set.create(text='Correct 1', value=1)
        self.wrong_choice1 = self.question1.choice_set.create(text='Wrong 1', value=0)

        self.player = self.quiz.player_set.create(name='Player1')
        self.player.current_question = self.question1
        self.player.position = 0
        self.player.save()

        self.timer = self.player.timer_set.create()
        self.timer.start()

    def test_can_access_by_url_name(self) -> None:
        """
        Test that update_game view can be accessed by url name
        <int:player_id>/<int:quiz_id>/<int:selected_difficulty>
        """
        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )
        response = self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_game_view(self) -> None:
        """
        Test that update_game redirects to game view when the player doesn't win yet
        """
        self.quiz.question_set.create(text='Question 2', number=2)
        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        url_redirect = reverse('quizer_game:game',
                               kwargs={'player_id': self.player.id,
                                       'quiz_id': self.quiz.id,
                                       'selected_difficulty': self.player.selected_difficulty
                                       }
                               )

        response = self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.assertRedirects(response, url_redirect)

    def test_redirect_to_result_view_when_time_is_up(self) -> None:
        """
        Test that update_game redirects to result view when the time is up (only in hard level)
        """
        self.player.selected_difficulty = 2
        self.player.save()

        self.timer.start_point = timedelta(seconds=0)
        self.timer.end_point = timedelta(seconds=63)
        self.timer.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        url_redirect = reverse('quizer_game:result',
                               kwargs={'player_id': self.player.id,
                                       'quiz_id': self.quiz.id,
                                       'selected_difficulty': self.player.selected_difficulty
                                       }
                               )

        response = self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.assertRedirects(response, url_redirect)

    def test_update_player_statuses_when_time_is_up(self) -> None:
        """
        Test that update_game update player statuses when the time is up (only in hard level)
        """
        self.player.selected_difficulty = 2
        self.player.save()

        self.timer.start_point = timedelta(seconds=0)
        self.timer.end_point = timedelta(seconds=63)
        self.timer.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.player.refresh_from_db()
        self.assertTrue(self.player.is_timeout)
        self.assertFalse(self.player.is_playing)

    def test_redirect_to_result_view_when_player_wins(self) -> None:
        """
        Test that update_game redirects to result view
        when the player wins (a racing car reaches the finish line)
        """
        self.player.position = 15
        self.player.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        url_redirect = reverse('quizer_game:result',
                               kwargs={'player_id': self.player.id,
                                       'quiz_id': self.quiz.id,
                                       'selected_difficulty': self.player.selected_difficulty
                                       }
                               )

        response = self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.assertRedirects(response, url_redirect)

    def test_update_player_statuses_when_player_wins(self) -> None:
        """
        Test that update_game update player statuses
        when the player wins (a racing car reaches the finish line)
        """
        self.player.position = 15
        self.player.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.player.refresh_from_db()
        self.assertTrue(self.player.is_achieved)
        self.assertFalse(self.player.is_playing)

    def test_redirect_to_result_view_when_player_answers_all_questions(self) -> None:
        """
        Test that update_game redirects to result view
        when the player already answered all questions
        """
        self.player.position = 10
        self.player.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        url_redirect = reverse('quizer_game:result',
                               kwargs={'player_id': self.player.id,
                                       'quiz_id': self.quiz.id,
                                       'selected_difficulty': self.player.selected_difficulty
                                       }
                               )

        response = self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.assertRedirects(response, url_redirect)

    def test_update_player_statuses_when_player_answers_all_questions(self) -> None:
        """
        Test that update_game update player statuses
        when the player already answered all questions
        """
        self.player.position = 10
        self.player.save()

        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        self.client.post(url, data={'choice_id': self.correct_choice1.id})
        self.player.refresh_from_db()
        self.assertTrue(self.player.is_failed)
        self.assertFalse(self.player.is_playing)

    def test_player_chooses_correct_answer(self):
        """
        When the player chooses correct answer, player's position will increase by 1
        """
        url = reverse('quizer_game:update',
                      kwargs={'player_id': self.player.id,
                              'quiz_id': self.quiz.id,
                              'selected_difficulty': self.player.selected_difficulty
                              }
                      )

        for i in range(3):
            with self.subTest(selected_difficulty=i):
                old_pos = self.player.position
                self.player.selected_difficulty = i
                self.player.save()

                self.client.post(url, data={'choice_id': self.correct_choice1.id})
                self.player.refresh_from_db()

                self.assertEqual(self.player.position, old_pos + 1)
    