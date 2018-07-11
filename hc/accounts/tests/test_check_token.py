from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        """test the check_token_submit page loads"""
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        """test it redirects to the checks page on successfully login"""
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_redirects_already_logged_in(self):
        """test that a logged in user redirects when they log in again"""
        # Login and test it redirects already logged in
        self.client.post(
            reverse(
                'hc-check-token',
                args=[
                    "alice",
                    "secret-token"]))
        re = self.client.post(
            reverse(
                'hc-check-token',
                args=[
                    "alice",
                    "secret-token"]))
        self.assertEqual(re.status_code, 302)
        self.assertRedirects(re, reverse("hc-checks"))

    def test_login_bad_token_redirects(self):
        """test that login with bad token redirects back to login page"""
        # Login with a bad token and check that it redirects
        response_bad_token = self.client.post(
            reverse('hc-check-token', args=["bob", "bad-token"]))
        self.assertRedirects(response_bad_token, reverse("hc-login"))
