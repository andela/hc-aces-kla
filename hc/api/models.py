# coding: utf-8

import hashlib
import json
import uuid
from datetime import timedelta as td
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from hc.api import transports
from hc.accounts.models import Profile
from hc.lib import emails

STATUSES = (
    ("up", "Up"),
    ("down", "Down"),
    ("new", "New"),
    ("paused", "Paused")
)
DEFAULT_TIMEOUT = td(days=1)
DEFAULT_GRACE = td(hours=1)
DEFAULT_NAG_TIME = td(days=1)
CHANNEL_KINDS = (("email", "Email"), ("webhook", "Webhook"),
                 ("hipchat", "HipChat"),
                 ("slack", "Slack"), ("pd", "PagerDuty"), ("po", "Pushover"),
                 ("victorops", "VictorOps"), ("twiliosms", "TwilioSms"),
                 ("twiliovoice", "TwilioVoice"))

PO_PRIORITIES = {
    -2: "lowest",
    -1: "low",
    0: "normal",
    1: "high",
    2: "emergency"
}


class Check(models.Model):

    class Meta:
        # sendalerts command will query using these
        index_together = ["status", "user", "alert_after", "number_of_nags"]

    name = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    timeout = models.DurationField(default=DEFAULT_TIMEOUT)
    grace = models.DurationField(default=DEFAULT_GRACE)
    n_pings = models.IntegerField(default=0)
    last_ping = models.DateTimeField(null=True, blank=True)
    alert_after = models.DateTimeField(null=True, blank=True, editable=False)
    status = models.CharField(max_length=6, choices=STATUSES, default="new")
    nag_intervals = models.DurationField(default=DEFAULT_NAG_TIME)
    nag_after_time = models.DateTimeField(null=True, blank=True)
    shopify = models.BooleanField(default=False)
    shopify_api_key = models.CharField(max_length=500, blank=True)
    shopify_password = models.CharField(max_length=500, blank=True)
    shopify_name = models.CharField(max_length=500, blank=True)
    runs_too_often = models.BooleanField(default=False)
    priority = models.IntegerField(default=1)
    number_of_nags = models.IntegerField(default=0)
    escalate = models.BooleanField(default=False)
    twilio_number = models.TextField(default="+00000000000", null=True,
                                     blank=True)

    def name_then_code(self):
        if self.name:
            return self.name
        return str(self.code)

    def url(self):
        return settings.PING_ENDPOINT + str(self.code)

    def log_url(self):
        return settings.SITE_ROOT + reverse("hc-log", args=[self.code])

    def email(self):
        return "%s@%s" % (self.code, settings.PING_EMAIL_DOMAIN)

    def send_alert(self):
        if self.status not in ("up", "down"):
            raise NotImplementedError("Unexpected status: %s" % self.status)
        if self.priority == 3 and self.number_of_nags < 4:
            self.escalate = False
        elif self.priority == 3 and self.number_of_nags > 3:
            self.escalate = True
        if self.priority == 2 and self.number_of_nags < 10:
            self.escalate = False
        elif self.priority == 2 and self.number_of_nags > 9:
            self.escalate = True
        self.number_of_nags += 1
        self.save()

        errors = []
        if self.escalate:
            # send alert to people on same team
            # send alert to people assigned to the check
            assigns = []
            if self.priority == 2:
                assigns = self.escalate_priority(9)
                # if self.number_of_nags > 9 and self.number_of_nags < 15:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=1)   
                #     if len(assigns) == 0:
                #         self.number_of_nags += 4
                #         self.save()
                # if self.number_of_nags > 14 and self.number_of_nags < 20:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=2)
                #     if len(assigns) == 0:
                #         self.number_of_nags += 4
                #         self.save()
                # if self.number_of_nags > 19:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=3)
            elif self.priority == 3:
                assigns = self.escalate_priority(3)
                # if self.number_of_nags > 3 and self.number_of_nags < 9:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=1)
                #     if len(assigns) == 0:
                #         self.number_of_nags += 4
                #         self.save()
                # if self.number_of_nags > 8 and self.number_of_nags < 14:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=2)
                #     if len(assigns) == 0:
                #         self.number_of_nags += 4
                #         self.save()
                # if self.number_of_nags > 13:
                #     assigns = Assigned.objects.filter(
                #         check_assigned=self, priority=3)
            if len(assigns) > 0:
                for assign in assigns:
                    user = User.objects.filter(id=assign.user_id).first()
                    channels = Channel.objects.filter(user=user)
                    for channel in channels:
                        error = channel.notify(self)
                        if error not in ("", "no-op"):
                            errors.append((channel, error))

            # find members in team of user
            # profile = Profile.objects.filter(user=self.user)
            # team_members = Profile.objects.filter(current_team=profile)
            # # get channels they ascribe to
            # for member in team_members:
            #     team_member = member.user
            #     print("====")
            #     print(member.user.id)
            #     print("xxxx")
            #     channels = Channel.objects.filter(user=team_member)
            #     for channel in channels:
            #         error = channel.notify(self)
            #         if error not in ("", "no-op"):
            #             errors.append((channel, error))

        else:
            for channel in self.channel_set.all():
                error = channel.notify(self)
                if error not in ("", "no-op"):
                    errors.append((channel, error))

        return errors

    def escalate_priority(self, n):
        assigns = []
        if self.number_of_nags > n and self.number_of_nags < (n + 6):
            assigns = Assigned.objects.filter(
                check_assigned=self, priority=1)
            if len(assigns) == 0:
                self.number_of_nags += 4
                self.save()
        if self.number_of_nags > (n + 5) and self.number_of_nags < (n + 11):
            assigns = Assigned.objects.filter(
                check_assigned=self, priority=2)
            if len(assigns) == 0:
                self.number_of_nags += 4
                self.save()
        if self.number_of_nags > (n + 10):
            assigns = Assigned.objects.filter(
                check_assigned=self, priority=3)   
        return assigns         

    def get_status(self):
        if self.status in ("new", "paused"):
            return self.status

        now = timezone.now()

        if self.last_ping + self.timeout + self.grace > now:
            return "up"

        return "down"

    def in_grace_period(self):
        if self.status in ("new", "paused"):
            return False

        up_ends = self.last_ping + self.timeout
        grace_ends = up_ends + self.grace
        return up_ends < timezone.now() < grace_ends

    def assign_all_channels(self):
        if self.user:
            channels = Channel.objects.filter(user=self.user)
            self.channel_set.add(*channels)

    def tags_list(self):
        return [t.strip() for t in self.tags.split(" ") if t.strip()]

    def to_dict(self):
        pause_rel_url = reverse("hc-api-pause", args=[self.code])

        result = {
            "name": self.name,
            "ping_url": self.url(),
            "pause_url": settings.SITE_ROOT + pause_rel_url,
            "tags": self.tags,
            "timeout": int(self.timeout.total_seconds()),
            "grace": int(self.grace.total_seconds()),
            "n_pings": self.n_pings,
            "status": self.get_status()
        }

        if self.last_ping:
            result["last_ping"] = self.last_ping.isoformat()
            result["next_ping"] = (self.last_ping + self.timeout).isoformat()
        else:
            result["last_ping"] = None
            result["next_ping"] = None

        return result


class Ping(models.Model):
    n = models.IntegerField(null=True)
    owner = models.ForeignKey(Check)
    created = models.DateTimeField(auto_now_add=True)
    scheme = models.CharField(max_length=10, default="http")
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    method = models.CharField(max_length=10, blank=True)
    ua = models.CharField(max_length=200, blank=True)


class Channel(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=20, choices=CHANNEL_KINDS)
    value = models.TextField(max_length=25, default="+256705357610")
    email_verified = models.BooleanField(default=False)
    checks = models.ManyToManyField(Check)

    def assign_all_checks(self):
        checks = Check.objects.filter(user=self.user)
        self.checks.add(*checks)

    def make_token(self):
        seed = "%s%s" % (self.code, settings.SECRET_KEY)
        seed = seed.encode("utf8")
        return hashlib.sha1(seed).hexdigest()

    def send_verify_link(self):
        args = [self.code, self.make_token()]
        verify_link = reverse("hc-verify-email", args=args)
        verify_link = settings.SITE_ROOT + verify_link
        emails.verify_email(self.value, {"verify_link": verify_link})

    @property
    def transport(self):
        if self.kind == "twiliosms":
            return transports.TwilioSms(self)
        if self.kind == "twiliovoice":
            return transports.TwilioVoice(self)
        if self.kind == "email":
            return transports.Email(self)
        elif self.kind == "webhook":
            return transports.Webhook(self)
        elif self.kind == "slack":
            return transports.Slack(self)
        elif self.kind == "hipchat":
            return transports.HipChat(self)
        elif self.kind == "pd":
            return transports.PagerDuty(self)
        elif self.kind == "victorops":
            return transports.VictorOps(self)
        elif self.kind == "pushbullet":
            return transports.Pushbullet(self)
        elif self.kind == "po":
            return transports.Pushover(self)
        else:
            raise NotImplementedError("Unknown channel kind: %s" % self.kind)

    def notify(self, check):
        # Make 3 attempts--
        for x in range(0, 3):
            error = self.transport.notify(check) or ""
            if error in ("", "no-op"):
                break  # Success!

        if error != "no-op":
            n = Notification(owner=check, channel=self)
            n.check_status = check.status
            n.error = error
            n.save()

        return error

    def test(self):
        return self.transport().test()

    @property
    def po_value(self):
        assert self.kind == "po"
        user_key, prio = self.value.split("|")
        prio = int(prio)
        return user_key, prio, PO_PRIORITIES[prio]

    @property
    def value_down(self):
        assert self.kind == "webhook"
        parts = self.value.split("\n")
        return parts[0]

    @property
    def value_up(self):
        assert self.kind == "webhook"
        parts = self.value.split("\n")
        return parts[1] if len(parts) == 2 else ""

    @property
    def slack_team(self):
        assert self.kind == "slack"
        if not self.value.startswith("{"):
            return None

        doc = json.loads(self.value)
        return doc["team_name"]

    @property
    def slack_channel(self):
        assert self.kind == "slack"
        if not self.value.startswith("{"):
            return None

        doc = json.loads(self.value)
        return doc["incoming_webhook"]["channel"]

    @property
    def slack_webhook_url(self):
        assert self.kind == "slack"
        if not self.value.startswith("{"):
            return self.value

        doc = json.loads(self.value)
        return doc["incoming_webhook"]["url"]

    def latest_notification(self):
        return Notification.objects.filter(channel=self).latest()


class Notification(models.Model):
    class Meta:
        get_latest_by = "created"

    owner = models.ForeignKey(Check)
    check_status = models.CharField(max_length=6)
    channel = models.ForeignKey(Channel)
    created = models.DateTimeField(auto_now_add=True)
    error = models.CharField(max_length=200, blank=True)


class Assigned(models.Model):
    check_assigned = models.ForeignKey(Check)
    user_id = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
