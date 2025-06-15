import main
from pathlib import Path


class MockEmailManager:
    """Capture outgoing emails instead of sending them."""

    def __init__(self, address: str) -> None:
        self.address = address
        self.sent_emails = []

    def send_email(
        self,
        to_addrs: list[str],
        subject: str,
        body: str,
        attachments: list[tuple[str, bytes]] = None,
    ) -> None:
        self.sent_emails.append(
            {
                "from": self.address,
                "to": to_addrs,
                "subject": subject,
                "body": body,
                "attachments": attachments or [],
            }
        )


def run_demo() -> None:
    # Use a separate data directory so real data isn't touched
    main.DATA_DIR = Path("demo_data")
    manager = MockEmailManager("touchstone@example.com")

    # ---- Sign ups ----
    # Alice creates a new group
    alice_signup = """First Name: Alice
Last Name: Anderson
Email: alice@example.com
"""
    main.handle_signup(manager, alice_signup)
    gid = main.find_group_for_email("alice@example.com")

    # Bob joins Alice's group using the provided group id
    bob_signup = f"""First Name: Bob
Last Name: Brown
Email: bob@example.com
Group Id: {gid}
"""
    main.handle_signup(manager, bob_signup)

    # Carol signs up without a group id and receives her own group
    carol_signup = """First Name: Carol
Last Name: Clark
Email: carol@example.com
"""
    main.handle_signup(manager, carol_signup)

    # ---- User updates ----
    group_messages = {}
    msg1 = {
        "from": "alice@example.com",
        "body": "Here is my update for this month.",
        "attachments": [],
    }
    msg2 = {
        "from": "bob@example.com",
        "body": "My update is attached!",
        "attachments": [("picture.jpg", b"fakeimage")],
    }
    main.handle_user_email(msg1, group_messages)
    main.handle_user_email(msg2, group_messages)

    # Compile and send report for each group
    for gid_key, msgs in group_messages.items():
        recipients = main.get_group_emails(gid_key)
        body, images = main.compile_report(msgs)
        manager.send_email(recipients, "Monthly Report", body, attachments=images)

    # Display captured emails
    for i, mail in enumerate(manager.sent_emails, 1):
        print(f"--- Email {i} ---")
        print(f"From: {mail['from']}")
        print(f"To: {', '.join(mail['to'])}")
        print(f"Subject: {mail['subject']}")
        print(f"Body:\n{mail['body']}\n")
        if mail["attachments"]:
            print(f"Attachments: {mail['attachments']}\n")


if __name__ == "__main__":
    run_demo()
