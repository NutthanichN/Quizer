from django.db import models
import time
from datetime import timedelta

# Create your models here.
DIFFICULTY = {0: 'Easy', 1: 'Medium', 2: 'Hard'}


class Quiz(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Topic')

    def __str__(self):
        return self.topic


# TODO question can contain image (and maybe audio file too)
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Quiz')
    text = models.CharField(max_length=200)
    number = models.IntegerField(default=0, verbose_name='Number')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question')
    text = models.CharField(max_length=200)
    value = models.IntegerField(default=0, verbose_name='Value')

    def __str__(self):
        return self.text


class Player(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, verbose_name='Quiz')
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Name')
    time = models.DurationField(default=timedelta(seconds=0), blank=True, verbose_name='Time spent')
    selected_difficulty = models.IntegerField(default=0, verbose_name='Difficulty')
    position = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False, verbose_name='Fail status')
    is_achieved = models.BooleanField(default=False, verbose_name='Achieve status')
    is_timeout = models.BooleanField(default=False, verbose_name='Timeout')
    correct_answer = models.IntegerField(default=0, verbose_name='Number of correct answers')
    wrong_answer = models.IntegerField(default=0, verbose_name='Number of wrong answers')
    
    def __str__(self):
        return self.name

    def move_forward(self):
        self.position += 1
        self.save()

    def move_backward(self):
        self.position -= 1
        self.save()

    def save_time_duration(self):
        timer = Timer.objects.get(player=self)
        self.time = timer.time_duration
        self.save()

    @property
    def total_answer(self):
        return self.correct_answer + self.wrong_answer

    @property
    def difficulty(self):
        return DIFFICULTY[self.selected_difficulty]


class Timer(models.Model):
    start_point = models.DurationField(default=timedelta(seconds=0), verbose_name='Start point')
    end_point = models.DurationField(default=timedelta(seconds=0), blank=True, verbose_name='Stop point')
    time_limit = models.DurationField(default=timedelta(seconds=0), blank=True, verbose_name='Time limit')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name='Player')

    def __str__(self):
        return f"A timer of {self.player}"

    def start(self):
        seconds = int(time.time())
        self.start_point = timedelta(seconds=seconds)
        self.save()

    def stop(self):
        seconds = int(time.time())
        self.end_point = timedelta(seconds=seconds)
        self.save()

    @property
    def time_duration(self):
        time_duration = abs(self.end_point - self.start_point)
        return time_duration

    def set_time_limit(self, seconds, minutes=0, hours=0):
        self.time_limit = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.save()
