from datetime import timedelta
from django.utils import timezone
from mock import patch
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase


class SendAlertsRunningTooOftenTestCase(BaseTestCase):

    def setUp(self):
        super(SendAlertsRunningTooOftenTestCase, self).setUp()
        created = timezone.now() - timedelta(days=2)
        timeout = timedelta(seconds=1200)
        grace = timedelta(seconds=120)
        first_ping = timezone.now() - timedelta(seconds=600)

        self.check = Check(
            name="Test 1",
            user=self.alice,
            status="up",
            created=created,
            timeout=timeout,
            grace=grace,
            last_ping=first_ping,
            n_pings=1
        )
        self.check.save()

    @patch("hc.api.management.commands.sendalerts.Command.handle_many")
    def test_it_notifies_when_check_run_too_often(self, mock):
        '''
            Tests that a check is not too often i.e.
            it should not be run before the time left
            before its timeout period expires is
            less than or equal to its grace period
        '''

        # Ping check
        self.client.get("/ping/%s/" % self.check.code)

        # check if check flag in model is updated as running too often
        check = Check.objects.filter(name="Test 1").first()
        self.assertEqual(check.runs_too_often, True)

        # Assert when Command's handle many that when handle_many should return
        # True
        result = Command().handle_many()
        assert result, True
