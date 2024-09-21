import json
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FloodRisk
from .serializers import FloodRiskSerializer

class FloodRiskPredictionView(APIView):
    def post(self, request):
        # Extract data from the request
        location = request.data.get('location')
        risk_percentage = request.data.get('risk_percentage')
        soil_type = request.data.get('soil_type')
        elevation = request.data.get('elevation')

        # Validate that all required fields are provided
        if not all([location, risk_percentage, soil_type, elevation]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate risk_percentage to ensure it's a non-negative number
        try:
            risk_percentage = float(risk_percentage)
            if risk_percentage < 0:
                return Response({"error": "Risk percentage must be a non-negative value."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Risk percentage must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize the location to title case for consistency
        location = location.title()

        # Check for existing flood risk data using a case-insensitive query
        existing_flood_risk = FloodRisk.objects.filter(location__iexact=location).first()
        if existing_flood_risk:
            # If the location exists, update the existing record with new data
            existing_flood_risk.risk_percentage = risk_percentage
            existing_flood_risk.soil_type = soil_type
            existing_flood_risk.elevation = elevation
            existing_flood_risk.save()  # Save changes to the database
            return Response({"message": "Flood risk data updated successfully"}, status=status.HTTP_200_OK)

        # If the location does not exist, create a new FloodRisk instance
        flood_risk = FloodRisk.objects.create(
            location=location,
            risk_percentage=risk_percentage,
            soil_type=soil_type,
            elevation=elevation
        )

        # Serialize the created instance to include it in the response
        serializer = FloodRiskSerializer(flood_risk)

        # Return a success message for the creation along with the serialized data
        return Response({
            "message": "Flood risk data created successfully",
            "flood_risk": serializer.data  # Include details of the created FloodRisk instance
        }, status=status.HTTP_201_CREATED)

class FloodRiskView(APIView):
    def get(self, request, location):
        # Normalize the requested location to title case for retrieval
        location = location.title()
        try:
            # Attempt to retrieve the FloodRisk instance using a case-insensitive query
            flood_risk = FloodRisk.objects.get(location__iexact=location)
            serializer = FloodRiskSerializer(flood_risk)  # Serialize the retrieved data
            data = serializer.data  # Extract serialized data

            # Load risk thresholds from a JSON file for risk categorization
            json_path = os.path.join(settings.BASE_DIR, 'flood_risk', 'risk_messages.json')
            with open(json_path) as f:
                thresholds = json.load(f)['thresholds']

            # Determine the risk category based on the risk percentage
            risk_percentage = data['risk_percentage']
            for threshold in thresholds:
                if risk_percentage <= threshold['max']:
                    data['risk_category'] = threshold['category']
                    data['additional_information'] = threshold['additional_information']
                    break

            # Add a URL for Google Maps to show the location
            data['map_url'] = f"https://www.google.com/maps/search/?api=1&query={location}"
            return Response(data)  # Return the data with risk information

        except FloodRisk.DoesNotExist:
            # If the location is not found, return a 404 error
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)
