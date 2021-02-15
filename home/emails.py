from django.conf import settings
from django.template.loader import get_template


from django.core.mail import send_mail


def send_email(recipient_list=None):
    subject = 'New student'
    message = "You've create a new student and add it to our database!"
    email_from = settings.EMAIL_HOST_USER

    template = get_template('email_templates/student_created.html')

    send_mail(subject, message, email_from, recipient_list,
              html_message=template.render(context={
                  'recipient_list': recipient_list,
              }))
