import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email_with_attachment(file_path, subject, body, send_to):
    send_from = os.getenv('FROM_EMAIL')
    password = os.getenv('PASSWORD')
    smtp = os.getenv('SMTP')
    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = send_to
    message['Subject'] = subject

    message.attach(MIMEText(body, "html"))

    with open(file_path, 'rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f"attachment; filename= {file_path}",
        )
    message.attach(part)
    mail = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp, 465, context=context) as server:
        server.login(send_from, password)
        server.sendmail(send_from, send_to, mail)
    print(f'Email sent to: {send_to}')

