from unittest.mock import patch

from web_app.tasks import check_unprocessed_outbox_events


class TestCheckUnprocessedOutboxEventsTask:
    @patch("web_app.tasks.OutboxEventsRepo")
    @patch("web_app.tasks.message_producer")
    def test_no_unprocessed_events(self, mock_message_producer, mock_outbox_repo):
        mock_outbox_repo.list_unprocessed.return_value = []

        check_unprocessed_outbox_events()

        mock_outbox_repo.list_unprocessed.assert_called_once()
        mock_message_producer.produce_event_message.assert_not_called()
        mock_outbox_repo.confirm_processed_for.assert_not_called()

    @patch("web_app.tasks.OutboxEventsRepo")
    @patch("web_app.tasks.message_producer")
    def test_with_unprocessed_events(self, mock_message_producer, mock_outbox_repo):
        mock_event_1 = type(
            "OutboxEvent",
            (),
            {"id": 1, "payload": {"key": "value1"}},
        )()
        mock_event_2 = type(
            "OutboxEvent",
            (),
            {"id": 2, "payload": {"key": "value2"}},
        )()
        mock_outbox_repo.list_unprocessed.return_value = [mock_event_1, mock_event_2]
        unprocessed_events_count = len(mock_outbox_repo.list_unprocessed.return_value)

        check_unprocessed_outbox_events()

        mock_outbox_repo.list_unprocessed.assert_called_once()
        assert (
            mock_message_producer.produce_event_message.call_count
            == unprocessed_events_count
        )
        mock_message_producer.produce_event_message.assert_any_call(
            mock_event_1.payload,
        )
        mock_message_producer.produce_event_message.assert_any_call(
            mock_event_2.payload,
        )
        assert (
            mock_outbox_repo.confirm_processed_for.call_count
            == unprocessed_events_count
        )
        mock_outbox_repo.confirm_processed_for.assert_any_call(mock_event_1)
        mock_outbox_repo.confirm_processed_for.assert_any_call(mock_event_2)
