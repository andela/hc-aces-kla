from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)

        self.assertRedirects(r, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    # Test that the team access works
    def test_team_access_works(self):
        form = {"kind": "email", "value": "bob@example.org"}
        url = "/accounts/switch_team/%s/" % self.alice.username
        self.client.login(username="bob@example.org", password="password")

        """ Bob switches to Alice's team """
        response = self.client.get(url)
        self.assertEqual(self.bobs_profile.current_team, self.profile)

        self.assertEqual(response.status_code, 302)

        url = "/integrations/add/"
        r = self.client.post(url, form)
        self.assertRedirects(r, "/integrations/")
        q = Channel.objects.filter(value="bob@example.org").first()
        """ Check that channel was created by bob who is on  alice's team"""
        self.assertEqual(q.user, self.alice)

    # Test that non-member of team cannot access
    def test_non_member_cannot_access(self):
        form = {"kind": "email", "value": "charlie@example.org"}
        url = "/accounts/switch_team/%s/" % self.alice.username
        self.client.login(username="charlie@example.org", password="password")

        url = "/integrations/add/"
        r = self.client.post(url, form)
        self.assertRedirects(r, "/integrations/")
        q = Channel.objects.filter(value="charlie@example.org").first()
        """Check that channel created by charlie is not assigned to alice"""
        self.assertNotEqual(q.user, self.alice)

    # Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "food", "value": "meat"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        assert r.status_code == 400
