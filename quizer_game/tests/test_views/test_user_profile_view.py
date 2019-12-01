from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User



from quizer_game.models import Quiz, Question, Choice, Player


class UserprofileTest(TestCase):


    def setUp(self):

        # set up client
        self.client = Client()
        self.username = "haha"
        self.password = "hoho"
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_can_view_user_profile_for_user(self):
        """Test that a user can view user profile"""

        self.client.force_login(self.user)
        url = reverse('quizer_game:user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/user-profile.html')

    def  test_can_view_user_profile_for_player(self):
        """Test that a player can not view user profile"""

        url = reverse('quizer_game:user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizer_game/login_result.html')
