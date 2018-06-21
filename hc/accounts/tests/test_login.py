from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        """test it sends login link to email address on login"""
        check = Check()
        check.save()

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302

        ## Assert that a user was created
        users = User.objects.all()
        self.assertEqual(len(users),1)
        self.assertEqual(users[0].email, "alice@example.org")

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')
        ## Assert contents of the email body
        self.assertIn('Hello', mail.outbox[0].body)

        ## Assert that check is associated with the new user
        user = User.objects.get(email="alice@example.org")
        checks = Check.objects.all()
        self.assertEqual(checks[0].user.username,user.username)


    def test_it_pops_bad_link_from_session(self):
        """Tests bad_link is popped from session"""
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ## Any other tests?

    def test_it_loads_login_page(self):
        """tests that the login page loads"""
        response = self.client.get("/accounts/login/")
        self.assertIn(b'Please enter your email address.', response.content)

    def test_it_redirects_when_password_given(self):
        """test that login redirects to checks dashboard when password is supplied"""
        marcus = User(email = "marcus@example.com")
        marcus.set_password("password")
        marcus.save()
        form = {"email": "marcus@example.com", "password":"password"}
        response = self.client.post('/accounts/login/', form, follow = True)
        self.assertRedirects(response, '/checks/')
        self.assertIn(b'Checks', response.content)

