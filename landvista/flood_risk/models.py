from django.db import models
import requests  # Import requests to make HTTP calls
from django.conf import settings  # Import settings to access project settings

class FloodRisk(models.Model):
    # Define the model for storing flood risk data

    # Location field to store the name of the location
    location = models.CharField(max_length=255, unique=True, null=False)

    # Risk percentage field to store the risk associated with the location
    risk_percentage = models.FloatField(null=False)

    # Soil type field to describe the type of soil in the location
    soil_type = models.CharField(max_length=100, null=False)

    # Elevation field to store the elevation of the location
    elevation = models.FloatField(null=False)

    # Geometry field to store location geometry as JSON (e.g-coordinates)
    geometry = models.JSONField(null=True)

    def __str__(self):
        # String representation of the model instance
        return f"{self.location} - Risk: {self.risk_percentage}%"

    def save(self, *args, **kwargs):
        # Override the default save method to automatically fetch geometry before saving
        self.geometry = self.get_geometry(self.location)  # Get geometry data for the location
        super().save(*args, **kwargs)  # Call the parent class's save method

    def get_geometry(self, location_name):
        # Fetch geometry data from Google Maps API using the provided location name
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"  # Base URL for the API
        params = {
            "address": location_name,  # Parameter for the location name
            "key": settings.GOOGLE_MAPS_API_KEY  # API key from settings
        }
        response = requests.get(base_url, params=params)  # Make the API request
        data = response.json()  # Parse the JSON response

        if data['status'] == 'OK':
            # If the response is successful, return the geometry data
            return data['results'][0]['geometry']
        return {}  # Return an empty dictionary if no valid geometry is found
