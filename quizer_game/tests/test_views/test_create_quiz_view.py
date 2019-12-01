from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User



from quizer_game.models import Quiz, Question, Choice, Player


class CreateQuizTest(TestCase):


    def setUp(self):

        # set up client
        self.client = Client()
        self.username = "Hello"
        self.password = "world"
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_can_view_create_quiz_user(self):
        """Test that a user can view create quiz"""

        self.client.force_login(self.user)
        url = reverse('quizer_game:create-question-set')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/create-question.html')

    def test_can_view_create_quiz_player(self):
        """Test that a player can not view edit quiz"""

        url = reverse('quizer_game:create-question-set')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/login_result.html')


