from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q # Этот импорт нужен для работы фильтров
from .models import Airline, Aircraft, Airport, Runway, Flight
from .serializers import (
    AirlineSerializer, AircraftSerializer, AirportSerializer, 
    RunwaySerializer, FlightSerializer
)

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all().order_by('name')
    serializer_class = AirlineSerializer

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all().order_by('model')
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all().order_by('city')
    serializer_class = AirportSerializer

class RunwayViewSet(viewsets.ModelViewSet):
    queryset = Runway.objects.all().order_by('airport', 'name')
    serializer_class = RunwaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['airport']

class FlightViewSet(viewsets.ModelViewSet):
    # Просто берем все рейсы из базы и сортируем их по времени
    queryset = Flight.objects.all().order_by('departure_time')
    serializer_class = FlightSerializer
    
    # Настройки поиска и фильтрации
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['flight_number', 'origin__city', 'destination__city', 'origin__iata_code', 'destination__iata_code']
    ordering_fields = ['departure_time', 'arrival_time', 'status', 'flight_number']
    filterset_fields = ['status', 'airline', 'origin', 'destination']