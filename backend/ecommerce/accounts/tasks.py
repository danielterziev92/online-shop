import dramatiq
from django.core.mail import send_mail
from django.template.loader import render_to_string

from ecommerce.settings import EMAIL_HOST_USER


@dramatiq.actor
def send_verification_email(email, code):
    html_content = render_to_string('emails/verification.html', {'code': code})

    send_mail(
        subject='Потвърдете вашия имейл',
        message='',
        html_message=html_content,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email]
    )
