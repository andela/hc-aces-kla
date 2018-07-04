
echo "Running release tasks"

if [ printenv DB == "postgres" ]; then 
  echo "Running Migrations"
  python manage.py makemigrations 
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
printenv DB
echo "Done running pre-release.sh"
