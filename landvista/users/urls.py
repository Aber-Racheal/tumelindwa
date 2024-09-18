from django.urls import path
from .views import UserRegistrationView, UserDetailView, add_user

urlpatterns = [
    path('add_user/', add_user, name='add_user'),
    path('users/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/<int:userId>/', UserDetailView.as_view(), name='user-detail'),
]