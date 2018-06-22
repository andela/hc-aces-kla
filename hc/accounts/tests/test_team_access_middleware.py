from django.contrib.auth.models import User
from django.test import TestCase
from hc.accounts.models import Profile


class TeamAccessMiddlewareTestCase(TestCase):

    def test_it_handles_missing_profile(self):
        """test it handles a missing profile"""
        user = User(username="ned", email="ned@example.org")
        user2 = User(username="nedi", email="nedii@example.org")
        user.set_password("password")
        user2.set_password("password")
        user.save()
        user2.save()

        self.client.login(username="ned@example.org", password="password")
        r = self.client.get("/about/")
        self.client.login(username="nedii@example.org", password="password")
        ### Assert the new Profile objects count
        assert Profile.objects.count() == 1
