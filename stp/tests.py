from django.test import TestCase
from django.urls import reverse


class SptViewTest(TestCase):
    def test_index_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertContains(response, "Hello world!")
