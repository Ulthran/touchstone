import os
import smtplib
import imaplib
import email
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from template_utils import render_template


class EmailManager:
    """Utility class for sending and receiving emails via Gmail."""

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    IMAP_SERVER = "imap.gmail.com"

    def __init__(self, address: str, app_password: str) -> None:
        self.address = address
        self.app_password = app_password

    def send_email(
        self,
        to_addrs: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
    ) -> None:
        """Send an email to the provided addresses."""
        message = MIMEMultipart()
        message["From"] = self.address
        message["To"] = ", ".join(to_addrs)
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        if attachments:
            for path in attachments:
                try:
                    filepath = Path(path)
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(filepath.read_bytes())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={filepath.name}",
                    )
                    message.attach(part)
                except Exception:
                    continue

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.address, self.app_password)
            server.sendmail(self.address, to_addrs, message.as_string())

    def fetch_messages(
        self,
        since: Optional[datetime] = None,
        subject_filter: Optional[str] = None,
    ) -> List[Dict[str, any]]:
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
                date_header = msg.get("Date")
                try:
                    date_val = email.utils.parsedate_to_datetime(date_header)
                except Exception:
                    date_val = datetime.utcnow()
                body, attachments = self._extract_parts(msg)
                messages.append(
                    {
                        "from": from_addr,
                        "subject": subject,
                        "body": body,
                        "date": date_val,
                        "attachments": attachments,
                    }
                )
            return messages

    @staticmethod
    def _extract_parts(
        msg: email.message.Message,
    ) -> Tuple[str, List[Tuple[str, bytes]]]:
        body = ""
        attachments: List[Tuple[str, bytes]] = []
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))
                if ctype == "text/plain" and "attachment" not in disp:
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        body = payload.decode(errors="ignore")
                elif part.get_content_maintype() == "image":
                    filename = part.get_filename() or "image"
                    payload = part.get_payload(decode=True)
                    if payload is not None:
                        attachments.append((filename, payload))
        else:
            payload = msg.get_payload(decode=True)
            if payload is not None:
                body = payload.decode(errors="ignore")
        return body, attachments


def compile_report(messages: List[Dict[str, any]]) -> Tuple[str, List[str]]:
    """Create a simple text report and gather attachment paths."""
    lines = ["Monthly Updates", "================", ""]
    attachments: List[str] = []
    for msg in messages:
        lines.append(f"From: {msg['from']}")
        lines.append(msg["body"])
        lines.append("")
        attachments.extend(msg.get("saved_images", []))
    return "\n".join(lines), attachments


if __name__ == "__main__":
    addr = os.environ.get("GMAIL_ADDRESS")
    pw = os.environ.get("GMAIL_APP_PASSWORD")
    recips = os.environ.get("RECIPIENTS", "").split(";")

    if not addr or not pw or recips == [""]:
        print("Set GMAIL_ADDRESS, GMAIL_APP_PASSWORD and RECIPIENTS env variables")
    else:
        manager = EmailManager(addr, pw)
        subject = "Monthly update request"
        body = render_template("update_request")
        manager.send_email(recips, subject, body)
        print("Update request sent.")

        replies = manager.fetch_messages(subject_filter=subject)
        if replies:
            report, images = compile_report(replies)
            report_subject = "Monthly Report"
            manager.send_email(recips, report_subject, report, attachments=images)
            print("Report sent.")
        else:
            print("No replies yet.")
