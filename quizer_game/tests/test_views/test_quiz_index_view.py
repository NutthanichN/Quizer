from django.test import TestCase
from django.urls import reverse

from quizer_game.models import Quiz


class QuizIndexTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Quiz.objects.create(topic='Quiz 1')
        Quiz.objects.create(topic='Quiz 2')
        Quiz.objects.create(topic='Quiz 3')

    def test_can_access_quiz_index_by_url_name(self) -> None:
        """
        Test that a quiz-index page can be accessed by url name
        """
        url = reverse('quizer_game:quiz-index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_quiz_index_uses_correct_template(self) -> None:
        """
        Test that a view renders `quiz-index.html`
        """
        url = reverse('quizer_game:quiz-index')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'quizer_game/quiz-index.html')

    def test_display_a_list_of_quiz(self) -> None:
        """
        Test that quizzes are displayed on template
        """
        url = reverse('quizer_game:quiz-index')
        response = self.client.get(url)
        quiz_list = list(response.context['quizzes'])
        expected_quiz_list = ['<Quiz: Quiz 1>', '<Quiz: Quiz 2>', '<Quiz: Quiz 3>']
        self.assertQuerysetEqual(quiz_list, expected_quiz_list)
