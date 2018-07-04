
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase" == "postgres" ]; then 
  echo "Running Migrations"
  export PATH="/usr/pgsql-9.4/lib:$PATH pip install --no-binary psycopg2 psycopg2"
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
echo "$dataBase"
echo "Done running pre-release.sh"
