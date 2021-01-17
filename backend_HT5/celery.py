import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_HT5.settings')

# инициализируем селери и читаем настройки из файла settings.py, все настройки с тегом SELERY
# app = Celery(include=['home.tasks']) кастомные таски из файла в каждой апликухи импортятся
app = Celery('django_project')
app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task(bind=True)
def simple_task(self):
    return 2+2


# команда для для запуска таски " celery -A backend_HT5.celery worker -l info "