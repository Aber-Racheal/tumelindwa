
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.utils import generate_confirmation_link,send_email
from django.http import HttpResponse
import logging
"""
Intializing OAuth client for Auth0
"""
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
def login(request):
    """
    This is for handling login requests, including account activation if needed
    """
    next_url = request.GET.get('next', reverse("index"))
    uid = request.GET.get('uid')
    token = request.GET.get('token')
    """
    Checking for account activation
    """
    if uid and token:
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully. You can now log in.')
        else:
            messages.error(request, 'The confirmation link is invalid or has expired.')
            """
            Redirecting to Autho for login
            """
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback") + f"?next={next_url}")
    )
def callback(request):
    """
    This is to handle the callback from Auth0
    and also getting token from Auth0
    and retrieving users info
    """
    token = oauth.auth0.authorize_access_token(request)
    user_info = token.get("userinfo")
    user = User.objects.filter(email=user_info["email"]).first()
    if user and user.is_active:
        auth_login(request, user)
        next_url = request.GET.get('next', reverse("index"))
        return redirect(next_url)
    elif user and not user.is_active:
        messages.error(request, "Please confirm your email address to activate your account.")
        return redirect("login")
    else:
        request.session['user_info'] = user_info
        return redirect("register")
"""
In this function handle registration"""

def register(request):
    user_info = request.session.get("user_info")
    if request.method == "POST":
        username = user_info["email"]
        password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=username, email=user_info["email"])
        if created:
            user.set_password(password)
            user.is_active = False
            user.save()
            send_confirmation_email(request, user)
            messages.success(request, "Please check your email to confirm your registration.")
            return redirect("login")
        else:
            messages.error(request, "User already exists.")
            return redirect("login")
    return render(request, "authentication/register.html", {"user_info": user_info})
def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
def index(request):
    return render(
        request,
        "authentication/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
def confirm_registration(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired.')
        return redirect('index')
def send_confirmation_email(request, user):
    confirmation_link=generate_confirmation_link(user,request)
    subject='confirm Your Registration'
    context={
        'user':user,
        'confirmation_link':confirmation_link
    }
    html_message = render_to_string('authentication/confirmation_email.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    send_mail(
        subject,
        plain_message,
       from_email,
        [to_email],
       html_message=html_message
    )
    if send_email(subject, user.email, context):
        logging.info(f"Confirmation email sent to {user.email}")
    else:
        logging.error(f"Failed to send confirmation email to {user.email}")

User = get_user_model()

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Email confirmed successfully')
    else:
        return HttpResponse('Email confirmation link is invalid or has expired')        