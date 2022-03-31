import pytest
from rest_framework.test import APIClient

from settings.celery import app


@pytest.fixture
def api() -> APIClient:
    return APIClient()


@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'gevent'


@pytest.fixture(scope='session')
def celery_config():
    return {
        'task_always_eager': True,
        'task_store_eager_result': True,
        'task_eager_propagates': True,
        'broker_backend': 'memory'
    }


@pytest.fixture(autouse=True, scope='session')
def patch_celery():
    app.conf.task_always_eager = True
    app.conf.task_store_eager_result = True
    app.conf.task_eager_propagates = True
