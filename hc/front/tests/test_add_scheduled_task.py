from hc.api.models import Task
from hc.test import BaseTestCase


class AddScheduledTaskTestCase(BaseTestCase):
    """
        This class contains tests to handle adding scheduled tasks
    """

    def test_it_works(self):
        """Test that a task can be added """
        url = "/accounts/profile/"
        form = {
            "name": "James backups",
            "task_type": "database_backups",
            "frequency": "daily",
            "receive_email_updates": "True",
            "database_backups": "1"
        }
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        assert Task.objects.count() == 1
