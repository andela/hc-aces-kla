
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase" == "postgres" ]; then 
  echo "Running Migrations"
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
echo printenv PATH
echo "Done running pre-release.sh"
