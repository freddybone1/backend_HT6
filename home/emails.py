from backend_HT5 import settings
from django.core.mail import send_mail


def send_email():
    subject = 'New student'
    message = "You've create a new student and add it to our database!"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['hoodback@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
