# Touchstone Email Manager

This repository contains a simple Python tool for sending and receiving
emails using Gmail. It is intended as a starting point for a monthly
newsletter or update workflow.

## Gmail Setup

Gmail requires that you use an **App Password** when connecting via
SMTP/IMAP. Follow these steps:

1. Enable 2-Step Verification on your account:
   <https://myaccount.google.com/security>
2. Create an App Password at:
   <https://myaccount.google.com/apppasswords>
3. Store the generated password in an environment variable named
   `TOUCHSTONE_GMAIL_APP_PASSWORD`.

## Email templates

All outgoing message bodies live in the `templates/` directory. Each
template is a plain text file that can be customised directly. At
runtime the scripts load these files and format them with any required
values before sending emails.

## Running on the command line

Set the following environment variables before running:

- `TOUCHSTONE_GMAIL_ADDRESS` – your full Gmail address.
- `TOUCHSTONE_GMAIL_APP_PASSWORD` – the App Password created above.
- `TOUCHSTONE_RECIPIENTS` – semicolon separated list of addresses to email.

Run the helper script directly for ad-hoc usage:

```bash
python email_manager.py
```

The script will send a request for updates to the recipients, fetch any
replies with the same subject, compile a basic text report, and send the
report back to everyone.

## Scheduling with cron

A minimal `main.py` script is provided for running the workflow
from a cron job. For example, to trigger it at noon on the first day
of each month add the following line to your crontab:

```
0 12 1 * * /usr/bin/python /path/to/main.py >> ~/touchstone.log 2>&1
```

This is a bare‑bones example and should be extended with proper error
handling and scheduling for production use.

## Example workflow

To see a sample signup and reporting process without sending real emails, run:
```bash
python mock_interactions.py
```
This script prints each outgoing message for review.

