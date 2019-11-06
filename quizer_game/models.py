from django.db import models

# Create your models here.


# class GameManager(models.Manager):
#     pass


class Quiz(models.Model):
    topic = models.CharField(max_length=200)

    def __str__(self):
        return self.topic


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
    name = models.CharField(max_length=200)
    time = models.TimeField(null=True, blank=True)
    selected_difficulty = models.IntegerField(default=0)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def move(self):
        pass
