from django.test import TestCase
from django.urls import reverse


class IndexTest(TestCase):
    def test_can_access_index_by_url_name(self):
        """
        Test that an index page can be access using url name
        """
        url = reverse('quizer_game:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_uses_correct_template(self):
        """
        Test that a view renders `index.html`
        """
        url = reverse('quizer_game:index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'quizer_game/index.html')
