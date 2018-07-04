
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase"=="postgres" ]; then 
  echo "Running Migrations"
  db:
  image: postgres:latest
  ports:
    - "5432"
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
echo $(printenv PATH)
echo "Done running pre-release.sh"
