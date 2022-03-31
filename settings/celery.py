import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

from django.conf import settings  # noqa

app = Celery('settings')

app.config_from_object('django.conf:settings')

app.conf.result_backend = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'
app.conf.broker_url = f'amqp://{settings.AMQP_USER}:{settings.AMQP_PASSWORD}@{settings.AMQP_HOST}:{settings.AMQP_PORT}/{settings.AMQP_VHOST}'

app.autodiscover_tasks()
