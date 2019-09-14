
import requests
import passwords


def send_notification(subject, text):
    passwords.get_entry('mailgun')
    mailgun_key = mailgun.custom_properties['apikey']

    requests.post(
        "https://api.mailgun.net/v3/sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org/messages",
        auth=("api", mailgun_key),
        data={"from": "Mailgun Sandbox <postmaster@sandbox251ead2c26cb4ebc912a952465022c6a.mailgun.org>",
              "to": "Carlos Ruiz <swsafetydance@gmail.com>",
              "subject": subject,
              "text": text}
    )
