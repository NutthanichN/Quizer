from django.test import TestCase
from quizer_game.models import Quiz, Question, Choice, Player

# Create your tests here.


class QuizModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Quiz.objects.create(topic='Python Programming')

    def test_topic_label(self):
        """
        Test verbose name of topic (CharField)
        """
        quiz = Quiz.objects.get(id=1)
        field_label = quiz._meta.get_field('topic').verbose_name
        self.assertEquals(field_label, 'Topic')

    def test_topic_max_length(self):
        """
        Test max length of topic (CharField)
        """
        quiz = Quiz.objects.get(id=1)
        field_max_length = quiz._meta.get_field('topic').max_length
        self.assertEquals(field_max_length, 200)
