from django.urls import path, include
from . import views
# from .views import confirm_registration
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback/", views.callback, name="callback"),
    path("register/", views.register, name="register"),
    path('api/', include('users.urls')),
    path('auth/confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
]