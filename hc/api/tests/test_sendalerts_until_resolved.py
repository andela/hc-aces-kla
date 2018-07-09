from datetime import timedelta
from django.utils import timezone
from hc.api.management.commands.sendalerts import Command
from hc.api.models import Check
from hc.test import BaseTestCase
from mock import patch


class SendAlertsUntilResolvedTestCase(BaseTestCase):

    @patch("hc.api.management.commands.sendalerts.Command.handle_one")
    def test_it_handles_unresolved(self, mock):
        tommorrow = timezone.now() + timedelta(days=1)
        nag_after_time = timezone.now() + timedelta(days=3)
        names = ["Check %d" % d for d in range(0, 3)]

        for name in names:
            check = Check(user=self.alice, name=name)
            check.alert_after = tommorrow
            check.status = "down"
            check.nag_after_time = nag_after_time
            check.save()

        result = Command().handle_many()
        self.assertEqual(result, True)  