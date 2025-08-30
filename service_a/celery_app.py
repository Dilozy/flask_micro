from celery import Celery

from config import CeleryConfig


celery_app = Celery("service_a")
celery_app.config_from_object(CeleryConfig)
celery_app.autodiscover_tasks(["tasks"])


def init_app_for_celery(flask_app, celery_app):
    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)
    celery_app.Task = ContextTask
