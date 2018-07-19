echo "Running release tasks"
echo "Running Migrations"
python manage.py makemigrations --merge
python manage.py migrate
python manage.py ensuretriggers
python manage.py sendalerts
echo "Done running pre-release.sh"

    
