from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class UnresolvedChecksTestCase(BaseTestCase):
    """class unresolved checks"""

    def setUp(self):
        super(UnresolvedChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice")
        self.check.save()

    def test_unresolved_checks_url_works(self):
        """Test the unresolved checks url works"""

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/unresolved_checks/")
        self.assertEqual(response.status_code, 200)

    def test_grace_checks_not_returned(self):
        """Test checks with status grace are not returned"""

        self.check.last_ping = timezone.now() - td(minutes=30)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/unresolved_checks/")
        self.assertNotIn("Alice", response)

    def test_only_unresolved_checks_are_returned(self):
        """Test checks with status down are the only ones returned"""

        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "down"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/unresolved_checks/")
        self.assertContains(response, "Alice")

    def test_checks_up_not_returned(self):
        """Test checks with status up are not returned"""

        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/unresolved_checks/")
        self.assertNotIn("Alice", response)
