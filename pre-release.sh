
echo "Running release tasks"
echo "Running Migrations"
heroku config:os.getenv("DATABASE_URL")
python manage.py makemigrations 
python manage.py migrate
python manage.py ensuretriggers
python manage.py sendalerts


echo "Done running pre-release.sh"
