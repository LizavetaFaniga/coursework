from rest_framework import serializers
from .models import Airline, Aircraft, Airport, Runway, Flight
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'

class AircraftSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(source='airline.name', read_only=True)

    class Meta:
        model = Aircraft
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class RunwaySerializer(serializers.ModelSerializer):
    active_flight = serializers.SerializerMethodField()
    status_text = serializers.SerializerMethodField()
    airport_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Runway
        fields = '__all__'

    def get_airport_full_name(self, obj):
        return f"{obj.airport.city} ({obj.airport.iata_code})"

    def get_current_flight(self, obj):
        now = timezone.now()
        time_window = timedelta(minutes=30) 
        
        dep_flight = Flight.objects.filter(
            departure_runway=obj,
            departure_time__gte=now - time_window,
            departure_time__lte=now + time_window
        ).first()
        if dep_flight:
            return dep_flight

        arr_flight = Flight.objects.filter(
            arrival_runway=obj,
            arrival_time__gte=now - time_window,
            arrival_time__lte=now + time_window
        ).first()
        if arr_flight:
            return arr_flight

        return None

    def get_active_flight(self, obj):
        flight = self.get_current_flight(obj)
        if flight:
            return f"{flight.flight_number} ({flight.get_status_display()})"
        return None

    def get_status_text(self, obj):
        if not obj.is_active:
            return "ЗАКРЫТА"
            
        flight = self.get_current_flight(obj)
        if flight:
            return f"ЗАНЯТА ({flight.flight_number})"
            
        return "СВОБОДНА"


class FlightSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(source='airline.name', read_only=True)
    aircraft_model = serializers.CharField(source='aircraft.model', read_only=True) # <--- ДОБАВЛЕНО
    aircraft_tail = serializers.CharField(source='aircraft.tail_number', read_only=True)
    origin_city = serializers.CharField(source='origin.city', read_only=True)
    destination_city = serializers.CharField(source='destination.city', read_only=True)
    departure_runway_name = serializers.CharField(source='departure_runway.name', read_only=True)
    arrival_runway_name = serializers.CharField(source='arrival_runway.name', read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

    def validate(self, data):
        dep_time = data.get('departure_time')
        arr_time = data.get('arrival_time')
        dep_runway = data.get('departure_runway')
        arr_runway = data.get('arrival_runway')

        if dep_time and arr_time and arr_time <= dep_time:
            raise serializers.ValidationError({"arrival_time": "Время прилета должно быть позже времени вылета."})

        time_window = timedelta(minutes=30)

        if dep_runway and dep_time:
            overlapping = Flight.objects.filter(
                departure_runway=dep_runway,
                departure_time__range=(dep_time - time_window, dep_time + time_window)
            ).exclude(id=self.instance.id if self.instance else None)
            
            if overlapping.exists():
                raise serializers.ValidationError({"departure_runway": "Полоса вылета занята другим рейсом (в пределах 30 минут)."})

        if arr_runway and arr_time:
            overlapping = Flight.objects.filter(
                arrival_runway=arr_runway,
                arrival_time__range=(arr_time - time_window, arr_time + time_window)
            ).exclude(id=self.instance.id if self.instance else None)
            
            if overlapping.exists():
                raise serializers.ValidationError({"arrival_runway": "Полоса прилета занята другим рейсом (в пределах 30 минут)."})

        return data