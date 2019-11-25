from django.test import TestCase
from quizer_game.models import Quiz, Question, Player, Timer
import time
from datetime import timedelta


class TimerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        quiz = Quiz.objects.create(topic='Python Programming')
        question = Question.objects.create(quiz=quiz,
                                           text='What is str?',
                                           number=1)
        player = Player.objects.create(quiz=quiz,
                                       current_question=question,
                                       name='Player1',
                                       selected_difficulty=0)
        Timer.objects.create(player=player)

    def setUp(self) -> None:
        quiz = Quiz.objects.create(topic='Python Programming')
        question = Question.objects.create(quiz=quiz,
                                           text='What is str?',
                                           number=1)
        player = Player.objects.create(quiz=quiz,
                                       current_question=question,
                                       name='Player2',
                                       selected_difficulty=0)
        self.timer = player.timer_set.create()

    def test_timer_name_should_end_with_its_player_name(self):
        timer = Timer.objects.get(id=1)
        self.assertEqual(str(timer), 'A timer of Player1')

    def test_start(self):
        default_value = self.timer._meta.get_field('start_point').default
        self.timer.start()
        self.assertNotEqual(self.timer.start_point, default_value)

    def test_stop(self):
        default_value = self.timer._meta.get_field('end_point').default
        self.timer.stop()
        self.assertNotEqual(self.timer.end_point, default_value)

    def test_time_duration(self):
        self.timer.start()
        time.sleep(5)
        self.timer.stop()
        self.assertEqual(self.timer.time_duration, timedelta(seconds=5))

    def test_set_time_limit(self):
        self.timer.set_time_limit(seconds=50)
        self.assertEqual(self.timer.time_limit, timedelta(seconds=50))
