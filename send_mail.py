import email
import smtplib
import ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = ""
password = ""

smtp_server = "smtp.gmail.com"
port = 587  # For starttls

# Create a secure SSL context
context = ssl.create_default_context()


class Sendmail:
    def __init__(self, username):
        self.username = username

    def send_text_mail(self, html_text, subject):
        receiver_email = "{}@asu.edu".format(self.username)
        # receiver_email = "ibatj7@gmail.com"
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        text = MIMEText(html_text, "html")
        message.attach(text)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context
        ) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

    def send_compelete_mail(self):
        receiver_email = "{}@asu.edu".format(self.username)
        # receiver_email = "ibatj7@gmail.com"
        message = MIMEMultipart("alternative")
        message["Subject"] = "[Job Application Completed]"
        message["From"] = sender_email
        message["To"] = receiver_email
        body = """Hi {},\
            Your Job applications has been completed!!
            """.format(
            self.username
        )
        message.attach(MIMEText(body, "plain"))
        filename = "{}.png".format(self.username)
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        text = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context
        ) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
