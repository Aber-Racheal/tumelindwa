from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer
import requests
import os

class SearchView(APIView):
    def post(self, request):
        location_name = request.data.get('location')
        if not location_name:
            return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)

        if not location_name.istitle():
            return Response({'error': 'Enter a valid location'}, status=status.HTTP_400_BAD_REQUEST)

        existing_location = Location.objects.filter(name=location_name).first()
        if existing_location:
            serializer = LocationSerializer(existing_location)
            return Response(serializer.data)

        api_key = os.getenv('AIzaSyBBYsZVdFOBv3is6gNS3SbHr_xWY4pkpV8')
        if not api_key:
            return Response({'error': 'Google Maps API key is not set'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location_name}&key={api_key}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            result = data['results'][0]
            location = Location.objects.create(
                name=location_name,
                latitude=result['geometry']['location']['lat'],
                longitude=result['geometry']['location']['lng']
            )
            serializer = LocationSerializer(location)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
