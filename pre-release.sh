
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase" == "postgres" ]; then 
  echo "Running Migrations"
  heroku run python manage.py makemigrations 
  heroku run python manage.py migrate
  heroku run python manage.py ensuretriggers
  heroku run python manage.py sendalerts
fi
echo "$dataBase"
echo "Done running pre-release.sh"
