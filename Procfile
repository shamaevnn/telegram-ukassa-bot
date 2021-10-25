release: python manage.py migrate --noinput
web: gunicorn --bind :$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker tub.asgi:application
worker: celery -A tub worker -P prefork --loglevel=INFO
beat: celery -A tub beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
