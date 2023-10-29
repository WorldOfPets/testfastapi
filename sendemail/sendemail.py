import smtplib
from email.message import EmailMessage

from celery import Celery
"""

celery -A sendemail.sendemail:celery worker --loglevel=INFO --pool=solo

celery -A sendemail.sendemail:celery flower

"""
#from config import SMTP_PASSWORD, SMTP_USER
SMTP_PASSWORD = "https://youtu.be/fm4LTvMyiwE?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&t=169"
SMTP_USER = "youemail@google.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('sendemail', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Натрейдил Отчет Дашборд'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊</h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)