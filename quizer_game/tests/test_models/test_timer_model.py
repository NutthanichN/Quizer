from django.test import TestCase
from quizer_game.models import Quiz, Question, Player, Timer
import time
from datetime import timedelta


class TimerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        quiz = Quiz.objects.create(topic='Python Programming')
        question = Question.objects.create(quiz=quiz, text='What is str?', number=1)
        player = Player.objects.create(quiz=quiz, current_question=question,
                                       name='Player1', selected_difficulty=0)
        Timer.objects.create(player=player)

    def setUp(self) -> None:
        quiz = Quiz.objects.create(topic='Python Programming')
        question = Question.objects.create(quiz=quiz, text='What is str?', number=1)
        player = Player.objects.create(quiz=quiz, current_question=question,
                                       name='Player2', selected_difficulty=0)
        self.timer = player.timer_set.create()
        self.timer.start()

    def test_str(self):
        timer = Timer.objects.get(id=1)
        self.assertEqual(str(timer), 'A timer of Player1')

    def test_start(self):
        self.timer.start()
        seconds = int(time.time())
        t1 = timedelta(seconds=seconds)
        self.assertEqual(self.timer.start_point, t1)

    def test_stop(self):
        self.timer.stop()
        seconds = int(time.time())
        t1 = timedelta(seconds=seconds)
        self.assertEqual(self.timer.start_point, t1)

    def test_time_duration(self):
        self.timer.start()
        t1 = timedelta(seconds=int(time.time()))
        time.sleep(5)
        self.timer.stop()
        t2 = timedelta(seconds=int(time.time()))
        self.assertEqual(self.timer.time_duration, abs(t2 - t1))
