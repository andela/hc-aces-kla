
echo "Running release tasks"
dataBase =$(printenv DB)
if ["$dataBase" == "postgres"] then
    echo "Running Migrations"
    python manage.py migrate
    python manage.py ensuretriggers
    python manage.py sendalerts
    celery -A hc worker -l info
    celery -A hc beat -l info
fi
echo $dataBase
echo "Done running pre-release.sh"
