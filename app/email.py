import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, body):
# try:
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Ensure you're using the correct port (465 for SSL)
    server.login(sender_email, sender_password)  # <-- Ensure you use the app password here
    # Sending the email (you can add your email content here)
    # server.sendmail(sender_email, "testsmp48@gmail.com.com", "Hello, this is a test email123!!.")
    e=server.sendmail(sender_email, to_email, message.as_string())
#  server.sendmail(sender_email,"testsmp48@gmail.com.com", message.as_string())
    print(e)
    # return e
 
    
# print(f"mail details{sender_email} and {sender_password}")
# except Exception as e:
#     print(f"Failed to send email: {e}")
# finally:
#     server.quit()
