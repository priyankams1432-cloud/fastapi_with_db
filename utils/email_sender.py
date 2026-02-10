import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
app_password=os.environ["APP_PASSWORD"]
sender_email=os.environ["SENDER_EMAIL"]
# Email credentials
def send_email(receiver_email: str, subject: str, content: str) -> str:
    """send an email to the receiver_email with the subject and content"""

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Email body
    msg.set_content(content)

    # Connect to Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # 587 is the TLS port
        server.starttls()  # Start TLS encryption
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"
