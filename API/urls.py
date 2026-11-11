from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirlineViewSet, AircraftViewSet, AirportViewSet, 
    RunwayViewSet, FlightViewSet
)

router = DefaultRouter()
router.register(r'airlines', AirlineViewSet)
router.register(r'aircrafts', AircraftViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'runways', RunwayViewSet)
router.register(r'flights', FlightViewSet, basename='flights')

urlpatterns = [
    path('', include(router.urls)),
]