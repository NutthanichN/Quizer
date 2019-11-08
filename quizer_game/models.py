from django.db import models

# Create your models here.


# class GameManager(models.Manager):
#     pass


class Quiz(models.Model):
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.topic

    def active_player(self):
        pass

    def find_active_player(self):
        pass

    def create_player(self, name, selected_difficulty):
        player = self.player_set.create(name=name, selected_difficulty=selected_difficulty, is_playing=True)
        player.save()
        return player


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Player(models.Model):
    # game difficulty: easy(0) medium(1) hard(2)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    time = models.TimeField(null=True, blank=True)
    selected_difficulty = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    is_playing = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def move_forward(self):
        self.position += 1
        self.save()

    def move_backward(self):
        self.position -= 1
        self.save()

    def finish_playing(self):
        self.is_playing = False
        self.save()
