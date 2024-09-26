from django.db import models

class LocationSearch(models.Model):
    location = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} - {'Success' if self.is_successful else 'Failed'}"

class Download(models.Model):
    location_search = models.ForeignKey(LocationSearch, on_delete=models.CASCADE, related_name='downloads')
    download_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download for {self.location_search.location} at {self.download_time}"
