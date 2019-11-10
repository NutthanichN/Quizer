from django.db import models

# Create your models here.


class Quiz(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Topic')

    def __str__(self):
        return self.topic

    def create_player(self, name, selected_difficulty):
        player = self.player_set.create(name=name, selected_difficulty=selected_difficulty, is_playing=True)
        return player


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
    time = models.TimeField(null=True, blank=True, verbose_name='Time spent')
    selected_difficulty = models.IntegerField(default=0, verbose_name='Difficulty')
    position = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False, verbose_name='Fail status')
    is_achieved = models.BooleanField(default=False, verbose_name='Achieve status')

    def __str__(self):
        return self.name

    def move_forward(self):
        self.position += 1

    def move_backward(self):
        self.position -= 1
