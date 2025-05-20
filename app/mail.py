import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path

def send_email(to_email):
# try:
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    template_path = Path(__file__).parent / "templates" / "mail_template.html"
    with open(template_path, "r", encoding="utf-8") as f:
     html_content = f.read()
     subject = "Approval Notification"

# Replace placeholders with actual values
    # html_content = html_content.replace("{{name}}", name)
    message["Subject"] = subject
    # message.attach(MIMEText(body, "plain"))
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Ensure you're using the correct port (465 for SSL)
    server.login(sender_email, sender_password)  # <-- Ensure you use the app password here
    # Sending the email (you can add your email content here)
    # server.sendmail(sender_email, "testsmp48@gmail.com.com", "Hello, this is a test email123!!.")
    e=server.sendmail(sender_email, to_email, message.as_string())
#  server.sendmail(sender_email,"testsmp48@gmail.com.com", message.as_string())
    print(e)
    # return e
 
    
