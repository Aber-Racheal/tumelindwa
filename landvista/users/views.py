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
import logging

def test_view(request):
    return HttpResponse("This is a test view.")
    """
    View to handle user registration via POST request.
    Handles user creation and sends a confirmation email upon successful registration.
    """
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            subject = 'Welcome to Landvista'
            confirmation_link = generate_confirmation_link(user, request)
            context = {
                'user': user.username,
                'confirmation_link': confirmation_link,
            }
            if send_email(subject,user.email,context,template_name='email_templates.html'):
               return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
@csrf_exempt
@api_view(['POST'])
def send_test_email(request):
    try:
        email = request.data.get("email")
        if not email:
            return Response({"message": "missing email"}, status=status.HTTP_400_BAD_REQUEST)
        subject = 'Invitation To LandVista Dashboard'
        html_message = render_to_string('email_templates.html', {
            'user': '',
            'confirmation_link': 'http://kishyalandvista@gmail.com/confirm/'
        })
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to_email = email
        """
        sending email using Django's send_mail function
        """
        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=html_message
        )
        return Response({'message': 'Invitation email sent successfully.'}, status=status.HTTP_200_OK)
    except smtplib.SMTPException as smtp_exception:
        logging.error(f'SMTPException: {smtp_exception}')
        return Response({'message': f'Failed to send email: {smtp_exception}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logging.error(f'General Exception: {e}')
        return Response({'message': f'Failed to send email: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














