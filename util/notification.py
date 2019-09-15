
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import passwords


def send_notification(subject, text):
    hotmail = passwords.get_entry('hotmail')
    msg = MIMEMultipart()
    message = text
    password = hotmail.password
    msg['From'] = hotmail.username
    msg['To'] = "swsafetydance@gmail.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.live.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg['To']))


def send_notification_mailgun(subject, text):
    mailgun = passwords.get_entry('mailgun')
    mailgun_key = mailgun.custom_properties['apikey']

    requests.post(
        "https://api.mailgun.net/v3/sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org/messages",
        auth=("api", mailgun_key),
        data={"from": "Mailgun Sandbox <postmaster@sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org>",
              "to": "Carlos Ruiz <swsafetydance@gmail.com>",
              "subject": subject,
              "text": text}
    )
