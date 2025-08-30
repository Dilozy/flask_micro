from celery_app import celery_app
from repositories import OutboxEventsRepo
from producer import publish_service_a_event_with
from misc import with_app_context


@celery_app.task
@with_app_context
def check_unprocessed_outbox_events():
    for event in OutboxEventsRepo.list_unprocessed():
        publish_service_a_event_with(event.payload)

        OutboxEventsRepo.confirm_processed_for(event)
