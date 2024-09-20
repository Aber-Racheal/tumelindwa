
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer
import requests
from django.conf import settings

class SearchView(APIView):
    def post(self, request):
        location_name = request.data.get('location')
        if not location_name:
            return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not location_name.istitle():
            return Response({'error': 'Enter a valid location'}, status=status.HTTP_400_BAD_REQUEST)

        existing_location = Location.objects.filter(name=location_name).first()

        if existing_location:
            soil_type = self.get_soil_type(existing_location.latitude, existing_location.longitude)
            elevation = self.get_elevation(existing_location.latitude, existing_location.longitude)

            serializer = LocationSerializer(existing_location, context={'soil_type': soil_type, 'elevation': elevation})
            response_data = serializer.data
            response_data.update({
                'soil_type': soil_type,
                'elevation': elevation
            })
            return Response(response_data, status=status.HTTP_200_OK)

        api_key = settings.GOOGLE_MAPS_API_KEY
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key={api_key}'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'error': 'Error communicating with geocoding service'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()

        if data.get('status') == 'OK':
            result = data['results'][0]
            latitude = result['geometry']['location']['lat']
            longitude = result['geometry']['location']['lng']

            soil_type = self.get_soil_type(latitude, longitude)
            elevation = self.get_elevation(latitude, longitude)

            location = Location.objects.create(
                name=location_name,
                latitude=latitude,
                longitude=longitude
            )

            serializer = LocationSerializer(location, context={'soil_type': soil_type, 'elevation': elevation})

            response_data = serializer.data
            response_data.update({
                'soil_type': soil_type,
                'elevation': elevation
            })

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_soil_type(self, latitude, longitude):
        soil_type_url = f'https://api-test.openepi.io/soil/type?lat={latitude}&lon={longitude}'
        soil_response = requests.get(soil_type_url)
        if soil_response.status_code == 200:
            soil_data = soil_response.json()
            return soil_data
        return None

    def get_elevation(self, latitude, longitude):
        api_key = settings.GOOGLE_MAPS_API_KEY
        elevation_url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={api_key}'
        elevation_response = requests.get(elevation_url)
        if elevation_response.status_code == 200:
            elevation_data = elevation_response.json()
            if 'results' in elevation_data and elevation_data['results']:
                return elevation_data['results'][0]['elevation']
        return None
