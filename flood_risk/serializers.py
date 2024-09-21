# flood_risk/serializers.py

from rest_framework import serializers
from .models import FloodRisk

class FloodRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodRisk
        fields = ['location', 'risk_percentage', 'soil_type', 'elevation', 'geometry']
