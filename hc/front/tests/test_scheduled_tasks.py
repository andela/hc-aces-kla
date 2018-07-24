from hc.api.models import Task, Backup
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
            "task_type": "database_backups",
            "frequency": "daily",
            "receive_email_updates": "True",
            "database_backups": "1"
        }

    def test_add_export_reports(self):
        """Test that report backups can be setup """
        self.client.login(username="alice@example.org", password="password")

        self.form.pop('database_backups')
        self.form['export_reports'] = '1'
        self.form['task_type'] = 'export_reports'

        response = self.client.post(self.url, self.form)
        self.assertIn(b"Reports will be exported periodically!",
                      response.content)
        self.assertEqual(response.status_code, 200)
        assert Task.objects.count() == 1

    def test_add_database_backups(self):
        """Test that report backups can be setup """
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(self.url, self.form)
        self.assertIn(b"Database backups have been setup!", response.content)
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

    def test_cannot_add_duplicate_database_backups(self):
        self.client.login(username="alice@example.org", password="password")

        self.client.post(self.url, self.form)
        response = self.client.post(self.url, self.form)

        # Assert that database backups are already present
        self.assertIn(b"Database backups are already setup!",
                      response.content)

    def test_cannot_add_duplicate_report_export_task(self):
        self.client.login(username="alice@example.org", password="password")

        self.form.pop('database_backups')
        self.form['export_reports'] = '1'
        self.form['task_type'] = 'export_reports'
        self.client.post(self.url, self.form)
        response = self.client.post(self.url, self.form)

        # Assert that reports are already exported
        self.assertIn(b"Report exports are already setup!",
                      response.content)

    def test_cannot_export_reports_if_not_allowed(self):
        self.client.login(username="alice@example.org", password="password")

        # Disable reports
        form = {"update_reports_allowed": False}
        self.client.post("/accounts/profile/", form)

        # Attempt to add a report
        self.form.pop('database_backups')
        self.form['export_reports'] = '1'
        response = self.client.post(self.url, self.form)

        # Assert that no task was added
        self.assertIn(b"Reports are not enabled for this profile!",
                      response.content)
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
        assert Backup.objects.count() == 0
