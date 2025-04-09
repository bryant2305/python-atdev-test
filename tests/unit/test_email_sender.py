from unittest.mock import Mock
import smtplib
from src.services.email_sender import send_email
# tests/unit/test_email_sender.py
def test_send_email(mocker):
    # Mock del context manager SMTP_SSL
    mock_smtp_ssl = mocker.patch("smtplib.SMTP_SSL")
    mock_server = mock_smtp_ssl.return_value.__enter__.return_value
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"PDF content"))

    send_email(
        "to@example.com",
        "Test Subject",
        "Test Body",
        "dummy.pdf"
    )

    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
