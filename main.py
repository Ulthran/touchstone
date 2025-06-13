import os
import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from email_manager import EmailManager

DATA_DIR = Path("data")
LAST_RUN_FILE = Path("last_processed.txt")


def generate_group_id() -> str:
    """Generate a unique 16 digit hexadecimal group id."""
    DATA_DIR.mkdir(exist_ok=True)
    while True:
        gid = uuid.uuid4().hex[:16]
        if not (DATA_DIR / gid).exists():
            return gid


def add_member(first: str, last: str, email: str, group_id: Optional[str] = None) -> str:
    """Add a member to a group, creating the group if needed.

    Returns the group id the member was added to.
    """
    if group_id is None or not (DATA_DIR / group_id).exists():
        group_id = generate_group_id()
        (DATA_DIR / group_id).mkdir(parents=True, exist_ok=True)

    members_path = DATA_DIR / group_id / "members.csv"
    new_file = not members_path.exists()
    with members_path.open("a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if new_file:
            writer.writerow(["first_name", "last_name", "email"])
        writer.writerow([first, last, email])
    return group_id


def group_exists(group_id: str) -> bool:
    """Return True if the given group id directory exists."""
    return (DATA_DIR / group_id).exists()


def get_group_emails(group_id: str) -> List[str]:
    """Read all member emails for the specified group."""
    members_path = DATA_DIR / group_id / "members.csv"
    if not members_path.exists():
        return []
    emails: List[str] = []
    with members_path.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row.get("email")
            if email:
                emails.append(email)
    return emails


def parse_signup(body: str) -> Optional[dict]:
    """Extract signup information from a form submission email."""
    info = {}
    for line in body.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip().lower()] = value.strip()
    if "email" not in info:
        return None
    return info


def handle_signup(manager: EmailManager, body: str) -> None:
    data = parse_signup(body)
    if not data:
        print("Invalid signup email - missing data")
        return

    requested_gid = data.get("group id")
    exists = bool(requested_gid and group_exists(requested_gid))
    first = data.get("first name", "")
    last = data.get("last name", "")
    email = data.get("email")

    gid = add_member(first, last, email, requested_gid if exists else None)
    print(f"Added {email} to group {gid}")

    if exists:
        # Send welcome email to all members of the existing group
        recipients = get_group_emails(gid)
        subject = "Welcome to the group"
        body = (
            f"{first} {last} has joined your group!\n"
            "Feel free to reach out and introduce yourselves."
        )
        manager.send_email(recipients, subject, body)
    else:
        # New group was created
        subject = "Welcome to Touchstone"
        body = (
            f"Welcome {first}! A new group has been created for you with id {gid}.\n"
            "If you were expecting to join an existing group, please let us know."
        )
        manager.send_email([email], subject, body)


def handle_user_email(msg: dict) -> None:
    """Placeholder for processing user emails."""
    print(f"Received user email from {msg['from']}")


def load_last_run() -> datetime:
    if LAST_RUN_FILE.exists():
        ts = LAST_RUN_FILE.read_text().strip()
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            pass
    return datetime.utcnow()


def save_last_run(time: datetime) -> None:
    LAST_RUN_FILE.write_text(time.isoformat())


def main() -> None:
    address = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not address or not password:
        raise RuntimeError("Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD env variables")

    manager = EmailManager(address, password)
    since = load_last_run()
    messages = manager.fetch_messages(since=since)
    for msg in messages:
        if msg["from"].lower() == "noreply@carrd.com":
            handle_signup(manager, msg["body"])
        else:
            handle_user_email(msg)
    save_last_run(datetime.utcnow())


if __name__ == "__main__":
    main()
