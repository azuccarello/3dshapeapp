from unittest.mock import MagicMock, patch

from src.sms.client import send_messages


@patch("twilio.rest.Client")
def test_send_messages_sends_one_sms_per_body(mock_client_class, monkeypatch):
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "AC123")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "secret")
    monkeypatch.setenv("TWILIO_FROM_NUMBER", "+15551234567")
    monkeypatch.setenv("TWILIO_TO_NUMBER", "+15557654321")

    mock_client = mock_client_class.return_value
    mock_client.messages.create.side_effect = [MagicMock(sid="SM1"), MagicMock(sid="SM2")]

    sids = send_messages(["first message", "second message"])

    assert sids == ["SM1", "SM2"]
    mock_client_class.assert_called_once_with("AC123", "secret")
    assert mock_client.messages.create.call_count == 2
    mock_client.messages.create.assert_any_call(
        body="first message", from_="+15551234567", to="+15557654321"
    )
    mock_client.messages.create.assert_any_call(
        body="second message", from_="+15551234567", to="+15557654321"
    )
