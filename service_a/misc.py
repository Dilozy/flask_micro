from functools import wraps

from app_factory import create_app


def with_app_context(task_func):
    @wraps(task_func)
    def wrapper(*args, **kwargs):
        app = create_app()
        with app.app_context():
            return task_func(*args, **kwargs)
    return wrapper