import os
import smtplib
import imaplib
import email
from datetime import datetime
from typing import List, Dict, Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailManager:
    """Utility class for sending and receiving emails via Gmail."""

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    IMAP_SERVER = "imap.gmail.com"

    def __init__(self, address: str, app_password: str) -> None:
        self.address = address
        self.app_password = app_password

    def send_email(self, to_addrs: List[str], subject: str, body: str) -> None:
        """Send an email to the provided addresses."""
        message = MIMEMultipart()
        message["From"] = self.address
        message["To"] = ", ".join(to_addrs)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.address, self.app_password)
            server.sendmail(self.address, to_addrs, message.as_string())

    def fetch_messages(
        self,
        since: Optional[datetime] = None,
        subject_filter: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """Fetch messages from the inbox matching the optional criteria."""
        with imaplib.IMAP4_SSL(self.IMAP_SERVER) as imap:
            imap.login(self.address, self.app_password)
            imap.select("INBOX")

            criteria = ["ALL"]
            if since:
                criteria.append(f'SINCE "{since.strftime("%d-%b-%Y")}"')
            if subject_filter:
                criteria.append(f'SUBJECT "{subject_filter}"')
            result, data = imap.search(None, *criteria)
            if result != "OK":
                return []

            messages = []
            for num in data[0].split():
                res, msg_data = imap.fetch(num, "(RFC822)")
                if res != "OK":
                    continue
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                from_addr = email.utils.parseaddr(msg.get("From"))[1]
                subject = msg.get("Subject", "")
                body = self._extract_body(msg)
                messages.append({
                    "from": from_addr,
                    "subject": subject,
                    "body": body,
                })
            return messages

    @staticmethod
    def _extract_body(msg: email.message.Message) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))
                if ctype == "text/plain" and "attachment" not in disp:
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        return payload.decode(errors="ignore")
        else:
            payload = msg.get_payload(decode=True)
            if payload is not None:
                return payload.decode(errors="ignore")
        return ""


def compile_report(messages: List[Dict[str, str]]) -> str:
    """Create a simple text report from fetched messages."""
    lines = ["Monthly Updates", "================", ""]
    for msg in messages:
        lines.append(f"From: {msg['from']}")
        lines.append(msg['body'])
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    addr = os.environ.get("GMAIL_ADDRESS")
    pw = os.environ.get("GMAIL_APP_PASSWORD")
    recips = os.environ.get("RECIPIENTS", "").split(";")

    if not addr or not pw or recips == [""]:
        print("Set GMAIL_ADDRESS, GMAIL_APP_PASSWORD and RECIPIENTS env variables")
    else:
        manager = EmailManager(addr, pw)
        subject = "Monthly update request"
        body = (
            "Hi friends,\n\n"
            "Please reply to this email with your monthly updates.\n\n"
            "Thanks!"
        )
        manager.send_email(recips, subject, body)
        print("Update request sent.")

        replies = manager.fetch_messages(subject_filter=subject)
        if replies:
            report = compile_report(replies)
            report_subject = "Monthly Report"
            manager.send_email(recips, report_subject, report)
            print("Report sent.")
        else:
            print("No replies yet.")
