echo "Running release tasks"
echo "Running Migrations"
python manage.py makemigrations --merge
python manage.py migrate
python manage.py ensuretriggers
echo "Done running pre-release.sh"

    
