import os
import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

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


def handle_signup(body: str) -> None:
    data = parse_signup(body)
    if not data:
        print("Invalid signup email - missing data")
        return
    group_id = data.get("group id")
    first = data.get("first name", "")
    last = data.get("last name", "")
    email = data.get("email")
    gid = add_member(first, last, email, group_id)
    print(f"Added {email} to group {gid}")


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
            handle_signup(msg["body"])
        else:
            handle_user_email(msg)
    save_last_run(datetime.utcnow())


if __name__ == "__main__":
    main()
