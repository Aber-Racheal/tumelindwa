# flood_risk/urls.py

from django.urls import path
from .views import FloodRiskPredictionView, FloodRiskView

urlpatterns = [
    path('predict-flood-risk/', FloodRiskPredictionView.as_view(), name='flood-risk-predict'),
    path('flood-risk/<str:location>/', FloodRiskView.as_view(), name='flood-risk'),
]
