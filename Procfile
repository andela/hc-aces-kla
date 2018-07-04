release: python manage.py migrate && python manage.py ensuretriggers && python manage.py sendalerts
web: gunicorn hc.wsgi:application