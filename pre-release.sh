echo "Running release tasks"
echo "Running Migrations"
python manage.py makemigrations --merge
python manage.py migrate
python manage.py ensuretriggers
python manage.py sendalerts
redis-server
celery -A hc worker -l info
celery -A hc beat -l info
echo "Done running pre-release.sh"

    
