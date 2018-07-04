
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase" == "postgres" ]; then 
  echo "Running Migrations"
  PATH=/usr/pgsql-9.3/lib:$PATH pip install psycopg2-binary
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
echo "$dataBase"
echo "Done running pre-release.sh"
