set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers=5
