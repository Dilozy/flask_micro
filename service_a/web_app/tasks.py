from celery import shared_task

from web_app.repositories import OutboxEventsRepo
from web_app.extensions import message_producer


@shared_task
def check_unprocessed_outbox_events():
    unprocessed_events = OutboxEventsRepo.list_unprocessed()
    
    if not unprocessed_events:
        return

    for event in unprocessed_events:
        message_producer.produce_event_message(event.payload)

        OutboxEventsRepo.confirm_processed_for(event)
