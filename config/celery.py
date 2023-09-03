from celery import Celery
from celery.schedules import crontab
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('config.celery_config')


app.conf.update(result_expires=3600)


app.conf.beat_schedule = {
    'Delete expired tokens from black list': {
        'task': 'account.tasks.clear_tokens',
        'schedule': crontab(hour='12', minute='00')
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')