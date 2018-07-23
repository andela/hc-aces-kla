from hc.api.models import Task
from hc.test import BaseTestCase


class ScheduledTaskTestCase(BaseTestCase):
    """
        This class contains tests to handle adding scheduled tasks
    """

    def setUp(self):
        super(ScheduledTaskTestCase, self).setUp()
        self.url = "/accounts/profile/"
        self.form = {
            "name": "Report backups",
            "task_type": "export_reports",
            "frequency": "daily",
            "receive_email_updates": "True",
            "database_backups": "1"
        }

    def test_it_works(self):
        """Test that a task can be added """
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(self.url, self.form)
        self.assertEqual(response.status_code, 200)
        assert Task.objects.count() == 1

    def test_it_setting_daily_task(self):
        """Test that a daily task can be added """
        self.client.login(username="alice@example.org", password="password")
        self.client.post(self.url, self.form)
        task = Task.objects.filter(frequency='daily').first()
        self.assertIsNotNone(task)

    def test_it_setting_weekly_task(self):
        """Test that a daily task can be added """
        self.client.login(username="alice@example.org", password="password")
        self.form['frequency'] = 'weekly'
        self.client.post(self.url, self.form)
        task = Task.objects.filter(frequency='weekly').first()
        self.assertIsNotNone(task)

    def test_it_setting_monthly_task(self):
        """Test that a monthly task can be added """
        self.client.login(username="alice@example.org", password="password")
        self.form['frequency'] = 'monthly'
        self.client.post(self.url, self.form)
        task = Task.objects.filter(frequency='monthly').first()
        self.assertIsNotNone(task)

    def test_cannot_export_reports_if_not_allowed(self):
        self.client.login(username="alice@example.org", password="password")

        # Disable reports
        form = {"update_reports_allowed": False}
        self.client.post("/accounts/profile/", form)

        # Attempt to add a report
        self.form.pop('database_backups')
        self.form['export_reports'] = '1'
        self.client.post(self.url, self.form)

        # Assert that no task was added
        assert Task.objects.count() == 0

    def test_remove_scheduled_task(self):
        self.client.login(username="alice@example.org", password="password")
        # Add scheduled task of backing up reports
        self.client.post(self.url, self.form)
        task = Task.objects.filter(name="Report backups").first()

        # Delete task
        remove_url = "/accounts/profile/scheduled_task/%s/remove/" % task.id
        self.client.post(remove_url)
        assert Task.objects.count() == 0
