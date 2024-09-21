from django.urls import path
from .views import SearchView


urlpatterns = [
   path('location/', SearchView.as_view(), name='location'),
   path('search/', SearchView.as_view(), name='search'),

]

