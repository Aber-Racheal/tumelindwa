from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_location, name='search_location'),
    path('download/', views.download_report, name='download_report'),
    path('stats/', views.statistics, name='statistics'),
]
