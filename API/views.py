from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q  # <--- ВОТ ЭТА СТРОЧКА
from .models import Airline, Aircraft, Airport, Runway, Flight
from .serializers import (
    AirlineSerializer, AircraftSerializer, AirportSerializer, 
    RunwaySerializer, FlightSerializer
)

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all().order_by('id') # <--- Сортировка по ID
    serializer_class = AirlineSerializer

class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all().order_by('id') # <--- Сортировка по ID
    serializer_class = AirportSerializer

class RunwayViewSet(viewsets.ModelViewSet):
    queryset = Runway.objects.all()
    serializer_class = RunwaySerializer

class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['flight_number', 'origin__city', 'destination__city', 'origin__iata_code', 'destination__iata_code']
    ordering_fields = ['departure_time', 'arrival_time', 'status', 'flight_number']
    filterset_fields = ['status', 'airline', 'origin', 'destination']

    def get_queryset(self):
        # 1. Находим аэропорт Санкт-Петербург (или любой другой по коду LED)
        try:
            spb_airport = Airport.objects.get(iata_code='LED')
        except Airport.DoesNotExist:
            return Flight.objects.none() # Если аэропорта нет, ничего не показываем

        # 2. Показываем только те рейсы, где вылет или прилет - это Пулково
        queryset = Flight.objects.filter(
            Q(origin=spb_airport) | Q(destination=spb_airport)
        ).order_by('departure_time')

        # 3. Если админ добавил фильтры через сайт, применяем их
        if self.request.query_params:
            if self.request.query_params.get('status'):
                queryset = queryset.filter(status=self.request.query_params.get('status'))
            if self.request.query_params.get('airline'):
                queryset = queryset.filter(airline=self.request.query_params.get('airline'))
            if self.request.query_params.get('origin'):
                queryset = queryset.filter(origin=self.request.query_params.get('origin'))
            if self.request.query_params.get('destination'):
                queryset = queryset.filter(destination=self.request.query_params.get('destination'))
                
        return queryset