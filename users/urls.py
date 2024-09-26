from django.urls import path
from .views import UserRegistrationView, UserDetailView, add_user,confirm_registration_view, UserListView

urlpatterns = [
    path('add_user/', add_user, name='add_user'),
    path('users/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/<int:userId>/', UserDetailView.as_view(), name='user-detail'),
    path('confirm-registration/<uidb64>/<token>/', confirm_registration_view, name='confirm_registration'),
    path('allusers/', UserListView.as_view(), name='User_List_View'),
]