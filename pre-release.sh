
echo "Running release tasks"

if [ "$DB" == "$postgres" ]; then 
  echo "Running Migrations"
  python manage.py makemigrations 
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi

echo "Done running pre-release.sh"
