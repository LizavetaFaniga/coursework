from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    iata_code = models.CharField(max_length=3, unique=True, verbose_name='Код IATA')
    icao_code = models.CharField(max_length=4, unique=True, null=True, blank=True, verbose_name='Код ICAO')
    country = models.CharField(max_length=100, verbose_name='Страна')

    class Meta:
        db_table = 'airlines'
        verbose_name = 'Авиакомпания'
        verbose_name_plural = 'Авиакомпании'

    def __str__(self):
        return f"{self.name} ({self.iata_code})"


class Aircraft(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT, related_name='aircrafts', verbose_name='Авиакомпания')
    model = models.CharField(max_length=100, verbose_name='Модель')
    tail_number = models.CharField(max_length=20, unique=True, verbose_name='Бортовой номер')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')

    class Meta:
        db_table = 'aircrafts'
        verbose_name = 'Самолет'
        verbose_name_plural = 'Самолеты'

    def __str__(self):
        return f"{self.tail_number} - {self.model}"


class Airport(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    iata_code = models.CharField(max_length=3, unique=True, verbose_name='Код IATA')
    icao_code = models.CharField(max_length=4, unique=True, null=True, blank=True, verbose_name='Код ICAO')
    city = models.CharField(max_length=100, verbose_name='Город')
    country = models.CharField(max_length=100, verbose_name='Страна')

    class Meta:
        db_table = 'airports'
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'

    def __str__(self):
        return f"{self.city} ({self.iata_code})"

class Runway(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='runways', verbose_name='Аэропорт')
    name = models.CharField(max_length=20, verbose_name='Название полосы')
    length_m = models.PositiveIntegerField(verbose_name='Длина (м)')
    surface = models.CharField(max_length=50, blank=True, null=True, verbose_name='Покрытие')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        db_table = 'runways'
        verbose_name = 'ВПП'
        verbose_name_plural = 'ВПП'
        unique_together = ('airport', 'name')

    def __str__(self):
        return f"{self.airport.iata_code} - {self.name}"


class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'По расписанию'
        DELAYED   = 'delayed',   'Задержан'
        BOARDING  = 'boarding',  'Посадка'
        DEPARTED  = 'departed',  'Вылетел'
        ARRIVED   = 'arrived',   'Прибыл'
        CANCELLED = 'cancelled', 'Отменен'

    flight_number = models.CharField(max_length=10, verbose_name='Номер рейса')
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT, verbose_name='Авиакомпания')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, verbose_name='Самолет')
    
    origin = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='departures', verbose_name='Откуда')
    destination = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arrivals', verbose_name='Куда')
    
    departure_time = models.DateTimeField(verbose_name='Время вылета')
    arrival_time = models.DateTimeField(verbose_name='Время прилета')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, verbose_name='Статус')
    gate = models.CharField(max_length=10, blank=True, null=True, verbose_name='Выход (гейт)')

    departure_runway = models.ForeignKey(Runway, on_delete=models.SET_NULL, null=True, blank=True, related_name='departing_flights', verbose_name='Полоса вылета')
    arrival_runway = models.ForeignKey(Runway, on_delete=models.SET_NULL, null=True, blank=True, related_name='arriving_flights', verbose_name='Полоса прилета')

    class Meta:
        db_table = 'flights'
        verbose_name = 'Рейс'
        verbose_name_plural = 'Рейсы'
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.flight_number} ({self.origin.iata_code} - {self.destination.iata_code})"