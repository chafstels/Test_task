from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags




def send_confirmation_email(email, code):
    activation_url = f'http://localhost:8000/api/account/activate/?u={code}'
    context = {'activation_url': activation_url}
    subject = 'Hello, please confirm your email.'
    html_message = render_to_string('email_activate.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'admin@gmail.com',
        [email],
        html_message=html_message,
        fail_silently=True
    )

def send_confirmation_password(email, code):
    activation_url = f'http://localhost:8000/api/account/reset-password/confirm/?u={code}'
    context = {'activation_url': activation_url}
    subject = 'Hello, please confirm the new password.'
    html_message = render_to_string('new_password.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'admin@gmail.com',
        [email],
        html_message=html_message,
        fail_silently=True
    )

