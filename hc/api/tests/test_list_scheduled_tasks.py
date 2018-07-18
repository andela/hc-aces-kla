from hc.api.models import Task, TaskSchedule
from hc.test import BaseTestCase


class ScheduledTasksTestCase(BaseTestCase):
    def setUp(self):
        super(ScheduledTasksTestCase, self).setUp()

        self.task1 = Task(profile=self.profile)
        self.task1.name = "Database Backups"
        self.task1.task_type = "database_backups"
        self.task1.frequency = "daily"
        self.task1.save()

        self.task2 = Task(profile=self.profile, name="Database Backups")
        self.task2.task_type = "export_reports"
        self.task1.frequency = "weekly"
        self.task2.save()

        self.sched_1 = TaskSchedule(task=self.task1, send_email_updates=False)
        self.sched_1.date_created = timezone.now()
        self.sched_1.next_run_date = self.sched_1.date_created + \
            td(days=1)
        self.sched_1.save()

        self.sched_2 = TaskSchedule(task=self.task2, send_email_updates=False)
        self.sched_2.date_created = timezone.now()
        self.sched_2.next_run_date = self.sched_2.date_created + \
            td(days=1)
        self.sched_2.save()

    def get(self):
        return self.client.get("/accounts/profile/")

    def test_it_works(self):
        self.client.login(username="alice@example.org", password="password")
        self.get()
        assert Task.objects.count() == 2
        assert TaskSchedule.objects.count() == 2

    def test_task_scheduled_next_run(self):
        self.client.login(username="alice@example.org", password="password")
        schedules = TaskSchedule.objects.all()
        print(schedules[0])
        assert schedules[0].next_run_date is not None

    def test_it_shows_only_users_checks(self):
        self.client.login(username="alice@example.org", password="password")
        self.get()

        # self.assertEqual(len(data["tasks"]), 2)
        # for task in data["tasks"]:
        #     self.assertEqual(task["profile"], self.profile)
