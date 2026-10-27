from django.contrib import admin
from .models import Airline, Aircraft, Airport, Runway, Flight

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code', 'country')

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('model', 'tail_number', 'airline', 'capacity')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code', 'city')

@admin.register(Runway)
class RunwayAdmin(admin.ModelAdmin):
    list_display = ('name', 'airport', 'length_m', 'is_active')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'origin', 'destination', 'departure_time', 'status')
    list_filter = ('status', 'airline')