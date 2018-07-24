from __future__ import absolute_import, unicode_literals

import csv
import os
import dropbox

from datetime import timedelta as td
from django.core import management
from django.utils import timezone
from django.conf import settings
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from hc.api.models import Check, Task, TaskSchedule, Backup

logger = get_task_logger(__name__)
current_dir = os.path.abspath(__file__)


def get_profile_tasks(task_type):
    tasks = Task.objects.filter(task_type=task_type)
    return tasks


def update_schedule(schedule, task):
    schedule.run_count = schedule.run_count + 1
    if task.frequency == "daily":
        schedule.next_run_date = schedule.date_created + td(days=1)
    elif task.frequency == "weekly":
        schedule.next_run_date = schedule.date_created + td(days=7)
    elif task.frequency == "monthly":
        schedule.next_run_date = schedule.date_created + td(days=30)

    schedule.save()


def save_backup(task, schedule, file_name):
    backup = Backup(
                task=task,
                schedule=schedule,
                file_name=file_name)
    backup.save()


def upload_csv_to_dropbox(file, path):
    dbox = dropbox.Dropbox(settings.DROPBOX_TOKEN)
    path = "/{}".format(path)

    with open(file, 'rb') as f:
        data = f.read()
    try:
        response = dbox.files_upload(
            data, path)
    except dropbox.exceptions.ApiError as error:
        print('Error', error)
        return None
    return response


@shared_task
@periodic_task(
    run_every=(crontab(minute='*/2')),
    name="run_db_backup",
    ignore_result=True
)
def run_db_backup():
    tasks = get_profile_tasks('database_backups')
    current_time = timezone.now().strftime("%Y_%m_%d %H-%M-%S")

    for task in tasks:
        schedule = TaskSchedule.objects.filter(task_id=task.id).first()
        file_name = "hc-db-backup-task#{}-{}.sql".format(
            task.id,
            current_time
        )
        if timezone.now() < schedule.next_run_date:
            management.call_command('dbbackup',
                                    '--output-filename={}'.format(file_name))

            update_schedule(schedule, task)

            logger.info("Backup successful")
            save_backup(task, schedule, file_name)
        else:
            logger.info("Backup not run, too early")


@shared_task
@periodic_task(
    run_every=(crontab(minute='*/3')),
    name="export_reports_as_csv"
)
def export_reports_as_csv():
    '''Export CSV file with status of checks at a given time'''
    tasks = get_profile_tasks('export_reports')
    current_time = timezone.now().strftime("%Y_%m_%d %H-%M-%S")
    for task in tasks:
        schedule = TaskSchedule.objects.filter(task_id=task.id).first()
        if timezone.now() < schedule.next_run_date:
            # For each task, find the checks to be exported to CSV
            checks = Check.objects.filter(
                user=task.profile.user).order_by("created")
            checks_dict = checks.values(
                        "name",
                        "last_ping",
                        "status",
                        "priority",
                        "escalate")
            path = os.path.join(os.path.dirname(
                os.path.dirname(current_dir)), 'csv_reports')

            if not os.path.exists(path):
                os.mkdir(path)
            filename = "hc-report-task#{}-{}.csv".format(
                task.id,
                current_time
            )
            filepath = os.path.join(path, filename)

            # Write to CSV file
            with open(filepath, 'w') as my_csv:
                fields = [
                    "name", "last_ping", "status", "priority", "escalate"]
                writer = csv.DictWriter(
                    my_csv,
                    fields,
                    restval='n/a',
                    )
                writer.writeheader()

                for check in checks_dict:
                    writer.writerow(check)

            response = upload_csv_to_dropbox(filepath, filename)
            logger.info(response)
            update_schedule(schedule, task)
        else:
            logger.info("Too early to export reports")
