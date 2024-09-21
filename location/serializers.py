from rest_framework import serializers
from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    soil_type = serializers.SerializerMethodField()
    elevation = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'searched_at', 'soil_type', 'elevation']

    def get_soil_type(self, obj):
        return self.context.get('soil_type', None)

    def get_elevation(self, obj):
        return self.context.get('elevation', None)
