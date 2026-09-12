import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        # Loads your credentials from the .env file
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        # We will send the email from yourself, to yourself
        self.receiver_email = os.getenv("EMAIL_SENDER")

    def send_email(self, subject, body):
        if not self.sender_email or not self.sender_password:
            print("Email credentials missing in .env file!")
            return False

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        try:
            # Connect to Gmail's secure SMTP server
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print("✅ Email sent successfully! Check your inbox.")
            return True
        except Exception as e:
            print(f"❌ Failed to send email. Error: {e}")
            return False