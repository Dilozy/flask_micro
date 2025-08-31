from celery import shared_task

from repositories import OutboxEventsRepo
from producer import MessageProducer


message_producer = MessageProducer()


@shared_task
def check_unprocessed_outbox_events():
    unprocessed_events = OutboxEventsRepo.list_unprocessed()
    
    if not unprocessed_events:
        return

    for event in unprocessed_events:
        message_producer.produce_event_message(event.payload)

        OutboxEventsRepo.confirm_processed_for(event)
