from rest_framework import viewsets, filters # pyright: ignore[reportMissingImports]
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .models import Airline, Aircraft, Airport, Runway, Flight
from .serializers import (
    AirlineSerializer, AircraftSerializer, AirportSerializer, 
    RunwaySerializer, FlightSerializer
)

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class RunwayViewSet(viewsets.ModelViewSet):
    queryset = Runway.objects.all()
    serializer_class = RunwaySerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().order_by('departure_time')
    serializer_class = FlightSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = ['flight_number', 'origin__city', 'destination__city', 'origin__iata_code', 'destination__iata_code']
    ordering_fields = ['departure_time', 'arrival_time', 'status', 'flight_number']
    filterset_fields = ['status', 'airline', 'origin', 'destination']