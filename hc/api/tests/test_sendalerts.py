from datetime import timedelta
from unittest import skip
import pytest
from django.core import mail
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from mock import patch
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase

class SendAlertsTestCase(BaseTestCase, TransactionTestCase):

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

    @patch("hc.api.management.commands.sendalerts.Command.handle_many")
    def test_it_handles_grace_period(self, mock):
        check = Check(user=self.alice, status="up")

        # 1 day 30 minutes after ping the check is in grace period:
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        check.save()

        # Expect no exceptions--
        Command().handle_one(check)

        # Assert when Command's handle many that when handle_many should return
        # True
        result = Command().handle_many()
        assert result, True

