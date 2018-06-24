from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)

        self.assertRedirects(response, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        channels = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(channels.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            response = self.client.get(url)
            self.assertContains(
                response,
                "Integration Settings",
                status_code=200)

    def test_team_access_works(self):
<<<<<<< HEAD
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        # login alice and add channel
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)
=======
        """An added team member should add a channel using the team profile"""
<<<<<<< HEAD
<<<<<<< HEAD
        form = {"kind": "email", "value": "bob@example.org"}
        url = "/accounts/switch_team/%s/" % self.alice.username
        self.client.login(username="bob@example.org", password="password")
        # Bob switches to Alice's team
        response = self.client.get(url)
        self.assertEqual(self.bobs_profile.current_team, self.profile)
>>>>>>> 777b28c... Replaced docstrings in test_add_channel.py with comments

        channel = Channel.objects.filter(value="alice@example.org")
        url_check = "/integrations/%s/checks/" % channel[0].code

<<<<<<< HEAD
        # Bob, alice's teammate tries to access Alice's channel
        self.client.login(username="bob@example.org", password="password")
        r = self.client.get(url_check)
        self.assertContains(r, "Assign Checks to Channel", status_code=200)
=======
        url = "/integrations/add/"
        response = self.client.post(url, form)
        self.assertRedirects(response, "/integrations/")
        channel = Channel.objects.filter(value="bob@example.org").first()
        # Check that channel was created by bob who is on  alice's team
        self.assertEqual(channel.user, self.alice)
>>>>>>> 777b28c... Replaced docstrings in test_add_channel.py with comments
=======
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

=======
>>>>>>> 4fdf9d8... Adjusted team access tests for Adding channel and checks
        self.client.login(username="alice@example.org", password="password")
        channel = Channel(
            user=self.alice,
            kind="email",
            value="alice@example.org")
        channel.save()
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")
        response = self.client.get("/integrations/")
        self.assertContains(response, "alice@example.org")
>>>>>>> 1207952... Adjusted test implementation for team access for added checks and channels

    def test_non_member_cannot_access(self):
<<<<<<< HEAD
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        # login alice and add channel
        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        channel_code = q[0].code
        print("test")
        print(channel_code)
        url_check = "/integrations/%s/checks/" % q[0].code

        # login with charlie who is not a member of alice's team
        # and try to assign checks to the channel added by Alice
        self.client.login(username="charlie@example.org", password="password")
        r = self.client.get(url_check)
        self.assertEqual(r.status_code, 403)
=======
        """A non-member should not access team profile to add channel"""

<<<<<<< HEAD
        url = "/integrations/add/"
<<<<<<< HEAD
        response = self.client.post(url, form)
        self.assertRedirects(response, "/integrations/")
        channel = Channel.objects.filter(value="charlie@example.org").first()
        # Check that channel created by charlie is not assigned to alice
        self.assertNotEqual(channel.user, self.alice)
>>>>>>> 777b28c... Replaced docstrings in test_add_channel.py with comments
=======
        form = {"kind": "email", "value": "alice@example.org"}
=======
>>>>>>> 4fdf9d8... Adjusted team access tests for Adding channel and checks
        self.client.login(username="alice@example.org", password="password")
        channel = Channel(
            user=self.alice,
            kind="email",
            value="alice@example.org")
        channel.save()
        self.client.logout()

        self.client.login(username="charlie@example.org", password="password")
        response = self.client.get("/integrations/")
        self.assertNotContains(response, "alice@example.org")
>>>>>>> 1207952... Adjusted test implementation for team access for added checks and channels

    # Test that bad kinds don't work
    def test_bad_kinds_dont_work(self):
        url = "/integrations/add/"
        form = {"kind": "food", "value": "meat"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        assert response.status_code == 400
