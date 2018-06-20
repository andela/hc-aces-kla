from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    def test_redirects_already_logged_in(self):
        """test that a logged in user redirects when they log in again""" 
        #Login and test it redirects already logged in
        self.client.post("/accounts/login/", {"email":"alice@example.org"},follow=True)
        re = self.client.post("/accounts/login/", {"email":"alice@example.org"},follow=True)
        self.assertEqual(re.status_code, 200)
        self.assertRedirects(re, "/accounts/login_link_sent/")

    def test_login_bad_token_redirects(self):
        """test that login with bad token redirects back to login page"""
        ### Login with a bad token and check that it redirects
        self.client.post("/accounts/login/", {"email":"bob@example.org"},follow=True)
        response_bad_token = self.client.post("/accounts/check_token/bob/bad-token/")
        self.assertRedirects(response_bad_token,"/accounts/login/")
    ### Any other tests?
