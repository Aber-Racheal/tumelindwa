from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from .forms import UserCreationForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from .utils import send_email, generate_confirmation_link
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import smtplib
from django.db import transaction 
import logging

def test_view(request):
    return HttpResponse("This is a test view.")
    """
    View to handle user registration via POST request.
    Handles user creation and sends a confirmation email upon successful registration.
    """

logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    """Retrieve a list of all users"""

    def get (self, request):
        users = User.objects.all()
        total_users = User.objects.all().count()
        serializer = UserRegistrationSerializer(users, many= True)
        return Response({"total_users": total_users,
                         "users": serializer.data})

    @transaction.atomic
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    user = serializer.save()
                    subject = 'Welcome to Landvista'
                    confirmation_link = generate_confirmation_link(user, request)
                    context = {
                        'user': user.username,
                        'confirmation_link': confirmation_link,
                    }
                    if send_email(subject, user.email, context, template_name='email_templates.html'):
                        user.save()
                        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
                    else:
                        raise Exception("Failed to send confirmation email")
                        
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                return Response({"message": "Failed to register user due to email sending issue"}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class UserDetailView(APIView):
    """
    View to retrieve, update, or delete a user by their ID.
    Handles GET, PUT, and DELETE requests for user details.
    """
    def get(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, userId):
        try:
            user = User.objects.get(id=userId)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
def add_user(request):
    """
    View to create a new user via a form submission.
    Handles both displaying the form and processing form submissions.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            if form.cleaned_data['is_superuser']:
                user.is_superuser = True
                user.is_staff = True
                user.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin:index')
    else:
        form = UserCreationForm()
    return render(request, 'users/email_templates.html', {'form': form})
    
def confirm_registration_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  
        user.save()
        messages.success(request, 'Your email has been confirmed. You can now log in.')
        return redirect('login') 
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
        return redirect('home')  