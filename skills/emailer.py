import smtplib
import logging
from email.mime.text import MIMEText
from core import config

log = logging.getLogger("moon.skills.emailer")


class Emailer:
    """Send basic emails via SMTP."""

    def send_email(self, to_addr: str, subject: str, body: str) -> str:
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = config.EMAIL_USER
            msg["To"] = to_addr

            with smtplib.SMTP(config.EMAIL_SMTP, 587) as server:
                server.starttls()
                server.login(config.EMAIL_USER, config.EMAIL_PASS)
                server.sendmail(config.EMAIL_USER, [to_addr], msg.as_string())
            log.info("Email sent to %s with subject %s", to_addr, subject)
            return "Email sent successfully."
        except Exception:
            log.exception("Email send failed.")
            return "Couldn't send email."
