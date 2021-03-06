from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neksflis.settings')

app = Celery('neksflis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'deactivate-unsubscribed-users': {
        'task': 'neksflis.account.tasks.deactivate_unsubscribed_users',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
    'charge-subscriptions': {
        'task': 'neksflis.subscription.tasks.charge_subscriptions',
        'schedule': crontab(minute=0, hour='*/6'),
        'args': (),
    },
    'create-new-period-items': {
        'task': 'neksflis.subscription.tasks.create_new_period_items',
        'schedule': crontab(minute=0, hour='*/3'),
        'args': (),
    },
    'cancel-unpaid-subscriptions': {
        'task': 'neksflis.subscription.tasks.cancel_unpaid_subscriptions',
        'schedule': crontab(minute=0, hour='*/6'),
        'args': (),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
