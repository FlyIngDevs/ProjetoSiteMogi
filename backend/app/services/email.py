import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import settings


def send_email_message(message: EmailMessage) -> None:
    """Send an email using the configured SMTP server."""
    if not settings.smtp_host or not settings.smtp_from_email:
        raise RuntimeError(
            "SMTP is not configured. Set SMTP_HOST and SMTP_FROM_EMAIL in backend/.env."
        )

    if settings.smtp_use_ssl:
        with smtplib.SMTP_SSL(
            settings.smtp_host,
            settings.smtp_port,
            context=ssl.create_default_context()
        ) as server:
            if settings.smtp_username:
                server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        return

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        if settings.smtp_use_tls:
            server.starttls(context=ssl.create_default_context())
        if settings.smtp_username:
            server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(message)
