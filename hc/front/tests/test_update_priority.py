from hc.api.models import Check
from hc.test import BaseTestCase


class UpdatePriorityTestCase(BaseTestCase):

    def setUp(self):
        super(UpdatePriorityTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_it_works(self):
        """
        test the update method works
        """
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": "high"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.priority == 3

    def test_team_access_works(self):
        """
        tests that team members have access to change priority
        """
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": "medium"}

        # Logging in as bob, not alice. Bob has team access so this
        # should work.
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url, data=payload)

        check = Check.objects.get(code=self.check.code)
        assert check.priority == 2

    def test_it_checks_ownership(self):
        """
        test it checks for ownership of a check
        """
        url = "/checks/%s/priority/" % self.check.code
        payload = {"priority": "low"}

        self.client.login(username="charlie@example.org", password="password")
        response = self.client.post(url, data=payload)
        assert response.status_code == 403

    def test_it_handles_bad_uuid(self):
        """
        tests bad uuid returns error
        """
        url = "/checks/not-uuid/priority/"
        payload = {"priority": "high"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        assert response.status_code == 400

    def test_it_handles_missing_uuid(self):
        """
        Valid UUID but there is no check for it
        """
        url = "/checks/6837d6ec-fc08-4da5-a67f-08a9ed1ccf62/priority/"
        payload = {"priority": "medium"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        assert response.status_code == 404
