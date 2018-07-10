from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td


class UpdateNagIntervalTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateNagIntervalTestCase, self).setUp()
        self.check = Check(user=self.alice)
        # self.check.nag_intervals = td(seconds=10000)
        self.check.save()

    def test_it_works(self):
        url = "/checks/%s/nag_interval/" % self.check.code
        payload = {"nag_interval": 5000}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEqual(check.nag_intervals.total_seconds(), 5000)
        assert check.nag_intervals.total_seconds() == 5000
