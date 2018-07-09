from django.db.models import Q


def get_running_checks(query):
    running_checks = query.filter(
        Q(status="up") | Q(status="down"))
    return running_checks
