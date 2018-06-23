from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        assert Check.objects.count() == 1

    # Test that team access works
    def test_team_access(self):
        url = "/checks/add/"
        self.client.login(username="bob@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        check = Check.objects.all()[0]
        """ Checks if check created by bob is assigned to alice's team """
        self.assertEqual(check.user, self.alice)
