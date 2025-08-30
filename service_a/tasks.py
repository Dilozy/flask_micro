from celery_app import celery_app


@celery_app.task()
def sum_two():
    return 1 + 1
