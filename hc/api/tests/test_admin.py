from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class ApiAdminTestCase(BaseTestCase):

    def setUp(self):
        super(ApiAdminTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

        # Set Alice to be staff and superuser
        self.alice.is_staff = True
        self.alice.is_superuser = True
        self.alice.save()

    def test_it_shows_channel_list_with_pushbullet(self):
        self.client.login(username="alice@example.org", password="password")

        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()

        # Assert for the push bullet
        retrieve = Channel.objects.all()
        self.assertEqual("pushbullet", retrieve[0].kind)
