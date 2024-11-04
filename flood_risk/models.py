from django.db import models
import requests  
from django.conf import settings 


class FloodRisk(models.Model):
    location = models.CharField(max_length=255, unique=True, null=False)
    risk_percentage = models.JSONField(null=False)
    soil_type = models.CharField(max_length=100, null=False)
    elevation = models.FloatField(null=False)
    geometry = models.JSONField(null=True)


    def __str__(self):
       
        return f"{self.location} - Risk: {self.risk_percentage}%"
        
    def save(self, *args, **kwargs):
        # Override the default save method to automatically fetch geometry before saving
        self.geometry = self.get_geometry(self.location) 
        super().save(*args, **kwargs)



    def get_geometry(self, location_name):
        # Fetch geometry data from Google Maps API using the provided location name
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"  
        params = {
            "address": location_name,  
            "key": settings.GOOGLE_MAPS_API_KEY 
        }
        response = requests.get(base_url, params=params)  
        data = response.json() 

        print(f"Requesting geometry for: {location_name}")  
        print("API Response:", data)

        if data['status'] == 'OK':
            return data['results'][0]['geometry']
        return {}  

    
    
