from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        assert Check.objects.count() == 1

    def test_team_access(self):
        self.client.login(username="bob@example.org", password="password")
        self.check = Check(user=self.alice, name="alice check")
        self.check.save()
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")
        response = self.client.get("/checks/")
        self.assertContains(response, "alice check", status_code=200)
