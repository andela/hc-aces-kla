release: bash ./pre-release.sh
web: gunicorn hc.wsgi:application
worker: celery -A hc worker -B -l info