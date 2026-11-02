from rest_framework import serializers # type: ignore
from .models import Airline, Aircraft, Airport, Runway, Flight

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class RunwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Runway
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(source='airline.name', read_only=True)
    aircraft_tail = serializers.CharField(source='aircraft.tail_number', read_only=True)
    origin_city = serializers.CharField(source='origin.city', read_only=True)
    destination_city = serializers.CharField(source='destination.city', read_only=True)
    departure_runway_name = serializers.CharField(source='departure_runway.name', read_only=True)
    arrival_runway_name = serializers.CharField(source='arrival_runway.name', read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'