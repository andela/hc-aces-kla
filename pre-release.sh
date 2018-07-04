
echo "Running release tasks"
dataBase=$(printenv DB)
if [ "$dataBase"=="postgres" ]; then 
  echo "Running Migrations"
  ln -s /tmp/.s.PGSQL.5432 /var/run/postgresql/.s.PGSQL.5432
  python manage.py migrate
  python manage.py ensuretriggers
  python manage.py sendalerts
fi
echo $dataBase
echo "Done running pre-release.sh"
