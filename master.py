import os
from datetime import datetime, timedelta

from email_manager import EmailManager, compile_report


def run_cycle() -> None:
    address = os.environ.get("GMAIL_ADDRESS")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    recipients_env = os.environ.get("RECIPIENTS", "")
    recipients = [r.strip() for r in recipients_env.split(";") if r.strip()]

    if not address or not password or not recipients:
        raise RuntimeError(
            "Set GMAIL_ADDRESS, GMAIL_APP_PASSWORD and RECIPIENTS env variables"
        )

    manager = EmailManager(address, password)
    request_subject = "Monthly update request"
    request_body = (
        "Hi friends,\n\n"
        "Please reply to this email with your monthly updates.\n\n"
        "Thanks!"
    )
    manager.send_email(recipients, request_subject, request_body)
    print("Update request sent.")

    since = datetime.utcnow() - timedelta(days=31)
    replies = manager.fetch_messages(since=since, subject_filter=request_subject)
    if replies:
        report = compile_report(replies)
        manager.send_email(recipients, "Monthly Report", report)
        print("Report sent.")
    else:
        print("No replies yet.")


def main() -> None:
    try:
        run_cycle()
    except Exception as exc:
        print(f"Error running cycle: {exc}")


if __name__ == "__main__":
    main()
