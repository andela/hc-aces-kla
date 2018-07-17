from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta as td
from django.core import management
from django.utils import timezone
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from django.conf import settings
from hc.api.models import Task, TaskSchedule

logger = get_task_logger(__name__)


def get_profile_tasks(task_type):
    tasks = Task.objects.filter(task_type=task_type)
    return tasks


@shared_task
@periodic_task(
    run_every=(crontab(hour='*/12')),
    name="run_db_backup",
    ignore_result=True
)
def run_db_backup():
    tasks = get_profile_tasks('database_backups')
    current_time = timezone.now().strftime("%Y_%m_%d %H-%M-%S")

    directory = settings.DBBACKUP_STORAGE_OPTIONS['location']
    if not os.path.exists(directory):
        os.makedirs(directory)

    for task in tasks:
        schedule = TaskSchedule.objects.filter(task_id=task.id).first()
        file_name = "hc-db-backup-task#{}-{}".format(
            task.id,
            current_time
        )
        if timezone.now() > schedule.next_run_date:
            management.call_command('dbbackup',
                                    '--output-filename={}'.format(file_name))

            schedule.run_count = schedule.run_count + 1
            if task.frequency == "daily":
                schedule.next_run_date = schedule.date_created + td(days=1)
            elif task.frequency == "weekly":
                schedule.next_run_date = schedule.date_created + td(days=7)
            elif task.frequency == "monthly":
                schedule.next_run_date = schedule.date_created + td(days=30)

            schedule.save()
            logger.info("Backup successful")
        else:
            logger.info("Backup not run, too early")


@shared_task
def export_reports_as_csv():
    pass
