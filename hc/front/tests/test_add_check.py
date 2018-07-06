from unittest import skip
from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    """This class contains tests to handle adding checks"""

    @skip("Needs fixing")
    def test_it_works(self):
        """Test that a check can be added """
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access(self):
        """A team member should access checks added by a teammate"""
        self.client.login(username="bob@example.org", password="password")
        self.check = Check(user=self.alice, name="alice check")
        self.check.save()
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")
        response = self.client.get("/checks/")
        self.assertContains(response, "alice check", status_code=200)
