import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
sender_email = "touchstone.mailing@gmail.com"  # Your full Gmail address
receiver_email = "ctbushman@gmail.com"  # Recipient email

# For Gmail, you need to create an App Password:
# 1. Enable 2-Step Verification: https://myaccount.google.com/security
# 2. Create App Password: https://myaccount.google.com/apppasswords
# Then use that App Password below instead of your regular password
app_password = os.environ.get("TOUCHSTONE_GMAIL_APP_PASSWORD")  # Replace with your App Password

# Create message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email from Python"

# Add message body
body = "This is a test email sent from Python."
message.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, app_password)
        server.send_message(message)
        print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
