from celery import Celery, Task

from config import CeleryConfig


def celery_init_app(flask_app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(CeleryConfig)
    celery_app.set_default()
    celery_app.autodiscover_tasks(["tasks"])
    flask_app.extensions["celery"] = celery_app
    return celery_app
