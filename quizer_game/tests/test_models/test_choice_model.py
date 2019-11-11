from django.test import TestCase
from quizer_game.models import Quiz, Question, Choice


class ChoiceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        quiz = Quiz.objects.create(topic='Python Programming')
        question = Question.objects.create(quiz=quiz, text='What is str?', number=1)
        Choice.objects.create(question=question, text='String', value=1)

    def test_question_label(self):
        """Test verbose name of question (ForeignKey)"""
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('question').verbose_name
        self.assertEquals(field_label, 'Question')

    def test_text_label(self):
        """Test verbose name of text (CharField)"""
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_value_label(self):
        """Test verbose name of value (IntegerField)"""
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'Value')

    def test_text_max_length(self):
        """Test max length of text (CharField)"""
        choice = Choice.objects.get(id=1)
        field_max_length = choice._meta.get_field('text').max_length
        self.assertEquals(field_max_length, 200)

    def test_value_default(self):
        """Test default value of value (IntegerField)"""
        choice = Choice.objects.get(id=1)
        field_default = choice._meta.get_field('value').default
        self.assertEquals(field_default, 0)
