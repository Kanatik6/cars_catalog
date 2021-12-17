import os
from celery import Celery
from celery.schedules import crontab


from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

    
app.conf.beat_schedule = {
    "check_celery": {
        "task": "cars.tasks.check",
        "schedule": crontab()
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')