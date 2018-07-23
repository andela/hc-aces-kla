from hc.test import BaseTestCase
from django.urls import reverse


class HelpCenterTestCase(BaseTestCase):
    def setUp(self):
        super(HelpCenterTestCase, self).setUp()

    def test_faq_works(self):
        self.client.login(username="alice@example.org", password="password")
        response = self.client.get(reverse("hc-faqs"))
        self.assertEqual(response.status_code, 200)

    def test_help_videos_work(self):
        self.client.login(username="alice@example.org", password="password")
        response = self.client.get(reverse("hc-help-videos"))
        self.assertEqual(response.status_code, 200)
