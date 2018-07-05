from datetime import timedelta
from unittest import skip
from django.core import mail
from django.utils import timezone
from django.core.urlresolvers import reverse
from mock import patch
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase


class SendAlertsTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_few(self, mock):
        yesterday = timezone.now() - timedelta(days=1)
        names = ["Check %d" % d for d in range(0, 10)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = yesterday
            check.status = "up"
            check.save()

        result = Command().handle_many()
        assert result, "handle_many should return True"

        handled_names = []
        for args, kwargs in mock.call_args_list:
            handled_names.append(args[0].name)

        assert set(names) == set(handled_names)
        # The above assert fails. Make it pass
        # no failure

    @skip("Ignore test for now")
    def test_it_handles_grace_period(self):
        check = Check(user=self.alice, status="up")

        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

        # Assert when Command's handle many that when handle_many should return
        # True
        result = Command().handle_many()
        assert result, "handle_many should return True"

    @skip("Ignore test for now")
    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_notifies_when_check_run_too_often(self, mock):
        '''
            Tests that a check is not too often i.e. it should not be run before the time left
            before its timeout period expires is less than or equal to its grace period
        '''

        # Empty the test outbox
        mail.outbox = []

        created = timezone.now() - timedelta(days=2)

        timeout = timedelta(seconds=1200)
        grace = timedelta(seconds=120)
        first_ping = timezone.now() - timedelta(seconds=600)

        print(first_ping)
        check = Check(
            name="Test 1",
            user=self.alice,
            status="up",
            created=created,
            timeout=timeout,
            grace=grace,
            last_ping=first_ping,
            n_pings=1
        )
        check.save()
        check.refresh_from_db()

        # Ping immediately
        self.client.get("/ping/%s/" % check.code)

        check = Check.objects.filter(name="Test 1")
        # check if email is sent
        self.assertEqual(len(mail.outbox), 1)

        # check if check flag in model is updated as running too often
        self.assertEqual(check.runs_too_often, True)

        # check status icon should be changed if it is deemed
        # to be running too often
        self.client.login(username="alice@example.org", password="password")
        response = self.client.get(reverse("hc-reports"))
        self.assertContains(response, "bell.svg")
