

from django.db import models


# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    soil_type = models.CharField(max_length=255, null=True, blank=True)  # Add this field if you want to store it
    elevation = models.FloatField(null=True, blank=True)  # Add this field for elevation
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




 

  


  


