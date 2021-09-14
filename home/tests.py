from django.test import TestCase


class TestViews(TestCase):
    def test_home(self):
        """
        Test get response and template of home view
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
