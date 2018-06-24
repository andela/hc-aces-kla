from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        assert Check.objects.count() == 1

<<<<<<< HEAD
    # Test that team access works
<<<<<<< HEAD
=======
=======
>>>>>>> 1207952... Adjusted test implementation for team access for added checks and channels
    def test_team_access(self):
        self.client.login(username="bob@example.org", password="password")
        self.check = Check(user=self.alice, name="alice check")
        self.check.save()
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")
<<<<<<< HEAD
        response = self.client.post(url)
        self.assertRedirects(response, "/checks/")
        check = Check.objects.all()[0]
        """ Checks if check created by bob is assigned to alice's team """
        self.assertEqual(check.user, self.alice)
>>>>>>> 777b28c... Replaced docstrings in test_add_channel.py with comments
=======
        response = self.client.get("/checks/")
        self.assertContains(response, "alice check", status_code=200)
>>>>>>> 1207952... Adjusted test implementation for team access for added checks and channels
