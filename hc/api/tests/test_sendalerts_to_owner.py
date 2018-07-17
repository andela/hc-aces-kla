from datetime import timedelta

from django.utils import timezone
from hc.api.models import Check, Channel
from hc.test import BaseTestCase
from mock import patch
from django.contrib.auth.hashers import make_password


def fake_twilio_notify():
    pass


class SendOwnerAlertsTestCase(BaseTestCase):

    def setUp(self):
        super(SendOwnerAlertsTestCase,  self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    @patch("hc.api.transports.TwilioSms.notify", fake_twilio_notify())
    def test_it_handles_check_owner(self):
        """
            test it sends notifications to assigned owner
        """
        channel = Channel(user=self.bob, kind="email",
                          value="bob@example.org")
        channel.save()
        check = Check(user=self.alice, status="down",
                      check_owner="bob@example.org")
        check.last_ping = timezone.now() - timedelta(minutes=30)
        check.number_of_nags = 2
        check.priority = 3
        check.save()
        check.send_alert()

        self.assertFalse(check.escalate)
        assert check.number_of_nags == 3
