from datetime import timedelta

from django.utils import timezone
from hc.api.models import Check, Channel
from hc.test import BaseTestCase
from mock import patch
from django.contrib.auth.hashers import make_password


def fake_twilio_notify():
    pass


class SendProtocolAlertsTestCase(BaseTestCase):

    def setUp(self):
        super(SendProtocolAlertsTestCase,  self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.channel = Channel(user=self.bob, kind="email",
                               value="bob@example.com")
        self.channel.save()
        self.check = Check(user=self.alice, status="down")
        self.check.last_ping = timezone.now() - timedelta(minutes=300)
        self.check.number_of_nags = 5
        self.check.priority = 3
        self.check.save()

    @patch("hc.api.transports.TwilioSms.notify", fake_twilio_notify())
    def test_it_handles_protocol_list(self):
        """
            test it escalates
        """
        self.check.send_alert()
        assert self.check.escalate
        assert self.check.number_of_nags == 6

    @patch("hc.api.transports.TwilioSms.notify", fake_twilio_notify())
    def test_it_handles_many_checks_protocol_list(self):
        """
            test it escalates
        """
        check1 = Check(user=self.alice, status="down")
        check2 = Check(user=self.alice, status="down")
        check1.last_ping = timezone.now() - timedelta(minutes=300)
        check2.last_ping = timezone.now() - timedelta(minutes=300)
        check1.number_of_nags = 15
        check2.number_of_nags = 5
        check1.priority = 2
        check2.priority = 2
        check1.save()
        check2.save()
        self.check.send_alert()
        check1.send_alert()
        check2.send_alert()

        assert check1.escalate
        assert check1.number_of_nags == 16
        assert check2.number_of_nags == 6
