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
        location = request.data.get('location')
        risk_percentage = request.data.get('risk_percentage')
        soil_type = request.data.get('soil_type')
        elevation = request.data.get('elevation')


        missing_fields = []
        if not location:
            missing_fields.append("location")
        if not risk_percentage:
            missing_fields.append("risk_percentage")
        if not soil_type:
            missing_fields.append("soil_type")
        if not elevation:
                missing_fields.append("elevation")
     
        if missing_fields:
            return Response({"error": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
            
        
        if not isinstance(risk_percentage, dict):
            return Response({"error": "Risk percentage must be a valid JSON object."}, status=status.HTTP_400_BAD_REQUEST)
        
        for season, value in risk_percentage.items():
            if not isinstance(value, (int, float)):
                return Response({"error": f"Risk percentage for {season} must be a number."}, status=status.HTTP_400_BAD_REQUEST)
            if value < 0:
                return Response({"error": f"Risk percentage for {season} must be a non-negative value."}, status=status.HTTP_400_BAD_REQUEST)
        
        location = location.title()
       

        existing_flood_risk = FloodRisk.objects.filter(location__iexact=location).first()
        if existing_flood_risk:
            existing_flood_risk.risk_percentage = risk_percentage
            existing_flood_risk.soil_type = soil_type
            existing_flood_risk.elevation = elevation
            existing_flood_risk.save() 
            return Response({"message": "Flood risk data updated successfully"}, status=status.HTTP_200_OK)
       
        try:
            flood_risk = FloodRisk.objects.create(
                location=location,
                risk_percentage=risk_percentage,
                soil_type=soil_type,
                elevation=elevation
            )

            seasonal_information = {}
            for season, risk in risk_percentage.items():
                risk_category = self.get_risk_category(season, risk)
                seasonal_information[season] = {
                     "risk_category": risk_category['category'],
                     "additional_information": risk_category['message']
                }
                
                serializer = FloodRiskSerializer(flood_risk)


            return Response({
                "message": "Flood risk data created successfully",
                "flood_risk": serializer.data,
                "seasonal_information": seasonal_information
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"Error occurred: {e}")
            return Response({"error": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def get_risk_category(self, season, risk_percentage):
        seasonal_json_path = os.path.join(settings.BASE_DIR, 'flood_risk', 'risk_messages.json')
        with open(seasonal_json_path) as f:
            seasonal_thresholds = json.load(f)

        for threshold in seasonal_thresholds[season]:
            if risk_percentage <= threshold['max']:
                return threshold
        return {"category": "unknown", "message": "Risk level is undetermined."}


class FloodRiskView(APIView):
    def get(self, request, location):
        location = location.title()
        try:
            flood_risk = FloodRisk.objects.get(location__iexact=location)
            serializer = FloodRiskSerializer(flood_risk) 
            data = serializer.data  
            
            seasonal_json_path = os.path.join(settings.BASE_DIR, 'flood_risk', 'risk_messages.json')
            with open(seasonal_json_path) as f:
                seasonal_thresholds = json.load(f)

            risk_messages_json_path = os.path.join(settings.BASE_DIR, 'flood_risk', 'risk_messages.json')
            with open(risk_messages_json_path) as f:
                risk_messages = json.load(f)

            seasonal_information = {}
            risk_percentage = data['risk_percentage']
            for season, risk in risk_percentage.items():
                risk_category = self.get_risk_category(season, risk, seasonal_thresholds)
                seasonal_information[season] = {
                    "risk_category": risk_category['category'],
                    "additional_information": risk_category['message']
                }

            data['seasonal_information'] = seasonal_information

            data['map_url'] = f"https://www.google.com/maps/search/?api=1&query={location}"
            return Response(data)  # Return the data with risk information
        except FloodRisk.DoesNotExist:
            # If the location is not found, return a 404 error
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, location):
        location = location.title()
        try:
            flood_risk = FloodRisk.objects.get(location__iexact=location)
            flood_risk.delete()
            return Response({"message": "Flood risk data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FloodRisk.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)



    def get_risk_category(self, season, risk_percentage, seasonal_thresholds):
        seasonal_json_path = os.path.join(settings.BASE_DIR, 'flood_risk', 'risk_messages.json')
        with open(seasonal_json_path) as f:
            seasonal_thresholds = json.load(f)

        for threshold in seasonal_thresholds[season]:
            if risk_percentage <= threshold['max']:
                return threshold
        return {"category": "unknown", "message": "Risk level is undetermined."}




