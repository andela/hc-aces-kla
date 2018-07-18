from django.core import mail
from django.core.urlresolvers import reverse

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check, Assigned


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        """tests that a set passowrd link is sent
        to the user's email address"""
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302
        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        # Assert that the token is set
        self.assertTrue(token)

        # Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Set password on healthchecks.io",
            mail.outbox[0].subject)
        self.assertIn("Here's a link to set a password", mail.outbox[0].body)

    def test_it_sends_report(self):
        """test that it sends a report about checks to the user email"""
        check = Check(name="Test Check", user=self.alice)
        check.save()

        self.alice.profile.send_report()

        # Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Monthly Report", mail.outbox[0].subject)
        self.assertIn(
            "This is a monthly report sent by healthchecks.io.",
            mail.outbox[0].body)

    def test_it_adds_team_member(self):
        """tests that a user can be added to a team"""
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        # Assert the existence of the member emails

        self.assertTrue("frank@example.org" in member_emails)

        # Assert that the email was sent and check email content
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "You have been invited to join alice@example.org",
            mail.outbox[0].subject)
        self.assertIn(
            "alice@example.org invites you to their healthchecks.io account.",
            mail.outbox[0].body)

    def test_add_team_member_checks_team_access_allowed_flag(self):
        """test that team access is allowed flag is true or false"""
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        """test that a team member can be removed"""
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        """test a team name can be set"""
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        """Test that team access allowed flag
        is checked when team name is set"""
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        """test usr can switch to own team"""
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        """test badges of user show in profile"""
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    # Test it creates and revokes API key
    def test_it_creates_and_revokes_api(self):
        """test that the api key can be set and revoked"""
        self.client.login(username="alice@example.org", password="password")
        self.client.session
        form = {"create_api_key": True, "show_api_key": True}
        response = self.client.post("/accounts/profile/", form)
        self.assertIn(b"The API key has been created!", response.content)

        form_1 = {"revoke_api_key": True}
        response_revoke = self.client.post("/accounts/profile/", form_1)
        self.assertIn(
            b"The API key has been revoked!",
            response_revoke.content)

    def test_it_updates_reports(self):
        """tests that reports can be updated"""
        self.client.login(username="alice@example.org", password="password")
        form = {"update_reports_allowed": False}
        response = self.client.post("/accounts/profile/", form)
        self.assertIn(b"Your settings have been updated!", response.content)

    # Test configuring reports for daily, weekly and monthly durations
    def test_configure_daily_reports(self):
        url = "/accounts/profile/"
        form = {
            "update_reports_allowed": True,
            "report_frequency": "day",
            "reports_allowed": True}
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        assert response.status_code == 200

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.report_frequency, "day")

    def test_configure_weekly_reports(self):
        url = "/accounts/profile/"
        form = {
            "update_reports_allowed": True,
            "report_frequency": "week",
            "reports_allowed": True}
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        assert response.status_code == 200

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.report_frequency, "week")

    def test_configure_monthly_reports(self):
        url = "/accounts/profile/"
        form = {
            "update_reports_allowed": True,
            "report_frequency": "month",
            "reports_allowed": True}
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        assert response.status_code == 200

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.report_frequency, "month")

    def test_it_loads_reports(self):
        """tests that reports can be updated"""
        self.client.login(username="alice@example.org", password="password")
        response = self.client.get(reverse("hc-reports"))
        self.assertIn(b"Today's Report", response.content)

    def test_it_assigns_check_to_member(self):
        """test that a team member can be removed"""
        self.check = Check(user=self.alice)
        self.check.save()
        print(self.check.code)
        self.client.login(username="alice@example.org", password="password")

        form = {"assign_checks": "1", "email": "bob@example.org",
                "check_code": self.check.code, "priority": 3}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Assigned.objects.count(), 1)
        assigned = Assigned.objects.filter(check_assigned=self.check).first()
        self.assertEqual(assigned.priority, 3)
        # self.bobs_profile.refresh_from_db()
        # self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_assigns_2_checks_to_one_member(self):
        """test that a team member can be removed"""
        self.check = Check(user=self.alice)
        self.check.save()
        self.check2 = Check(user=self.alice)
        self.check2.save()
        self.client.login(username="alice@example.org", password="password")

        form = {"assign_checks": "1", "email": "bob@example.org",
                "check_code": self.check.code, "priority": "3"}
        self.client.post("/accounts/profile/", form)
        form1 = {"assign_checks": "1", "email": "bob@example.org",
                 "check_code": self.check2.code, "priority": "3"}
        r = self.client.post("/accounts/profile/", form1)
        assert r.status_code == 200

        self.assertEqual(Assigned.objects.count(), 2)
        assigned = Assigned.objects.filter(check_assigned=self.check).first()
        print(assigned.check_assigned)
        if assigned.check_assigned:
            print("Here It is")
        else:
            print("Splash")    
        self.assertEqual(assigned.user_id, 32)

    def test_it_unassign_check_from_members(self):
        """test that a team member can be removed"""
        self.check = Check(user=self.alice)
        self.check.save()
        print(self.check.code)
        self.client.login(username="alice@example.org", password="password")

        form = {"assign_checks": "1", "email": "bob@example.org",
                "check_code": self.check.code, "priority": 3}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(Assigned.objects.count(), 1)
        
        form = {"unassign_check": "1", "email": "bob@example.org",
                "check_code": self.check.code}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(Assigned.objects.count(), 0)

    # def test_it_assign_check_to_same_user_twice(self):
        # """test that a team member can be removed"""
        # self.check = Check(user=self.alice)
        # self.check.save()
        # print(self.check.code)
        # self.client.login(username="alice@example.org", password="password")

        # form = {"assign_checks": "1", "email": "bob@example.org",
        #         "check_code": self.check.code, "priority": 3}
        # r = self.client.post("/accounts/profile/", form)
        # self.assertEqual(Assigned.objects.count(), 1)

        # form = {"unassign_check": "1", "email": "bob@example.org",
        #         "check_code": self.check.code}
        # r = self.client.post("/accounts/profile/", form)
        # self.assertEqual(Assigned.objects.count(), 0)   
