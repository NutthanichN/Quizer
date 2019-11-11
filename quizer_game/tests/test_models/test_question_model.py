from django.test import TestCase
from quizer_game.models import Quiz, Question


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        quiz = Quiz.objects.create(topic='Python Programming')
        Question.objects.create(quiz=quiz, text='What is str?', number=1)

    def test_quiz_label(self):
        """Test verbose name of quiz (ForeignKey)"""
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('quiz').verbose_name
        self.assertEquals(field_label, 'Quiz')

    def test_text_label(self):
        """Test verbose name of text (CharField)"""
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_number_label(self):
        """Test verbose name of number (IntegerField)"""
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('number').verbose_name
        self.assertEquals(field_label, 'Number')

    def test_text_max_length(self):
        """Test max length of text (CharField)"""
        question = Question.objects.get(id=1)
        field_max_length = question._meta.get_field('text').max_length
        self.assertEquals(field_max_length, 200)

    def test_number_default(self):
        """Test default value of number (IntegerField)"""
        question = Question.objects.get(id=1)
        field_default = question._meta.get_field('number').default
        self.assertEquals(field_default, 0)
