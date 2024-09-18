from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
import smtplib
import logging
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site


def send_email(subject, to_email, context, template_name='email_templates.html'):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    email_message = EmailMessage(
        subject,
        plain_message,
        from_email,
        [to_email]
    )
    email_message.content_subtype = 'html'
    try:
        email_message.send()
        logging.info(f"Email sent to {to_email} with subject '{subject}'")
        return True
    except Exception as e:
        logging.error(f'Failed to send email: {e}')
        return False

def generate_confirmation_link(user, request):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return request.build_absolute_uri(
        reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token})
    )




