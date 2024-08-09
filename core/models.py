from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import datetime as DateTime
from django.db.models import Q
from django.db.models import Sum
from django.utils.crypto import get_random_string

# Create your models here.


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    
    class Meta:
        abstract = True 


class Airport(BaseModel):
    
    airport_name = models.CharField(max_length=200)
    airport_city = models.CharField(max_length=50)
    airport_country = models.CharField(max_length=16)

    iata_code = models.CharField(max_length=3)
    icao_code = models.CharField(max_length=4)

    airport_type = models.CharField(max_length=14, null=True, blank=True)


    def get_all_flights_from_airport(self):
        return list(Flight.objects.filter(Q(origin_airport=self) | Q(destination_airport=self)).values())

        
    def __str__(self) -> str:
        return self.airport_name + " (" + self.iata_code + ")"


class Flight(BaseModel):

    flight_number = models.CharField(max_length=6)

    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flight_origin")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flight_destination")

    # departure
    departure_date = models.DateField()
    departure_time = models.TimeField()
    # arrival
    arrival_date = models.DateField()
    arrival_time = models.TimeField()


    def search_flight_result(self, seat_class):
        FMT = "%Y-%m-%d %H:%M:%S"
        x = 0
        if seat_class == 'all':
            x = 1
            seat_class = 'economy_fare'
        data = {
            "flight_number" : self.flight_number,
            "flight_id" : self.uid,
            "origin_airport" : {
                'airport_name' : self.origin_airport.airport_name,
                'airport_city' : self.origin_airport.airport_city,
                'airport_country' : self.origin_airport.airport_country, 
                'iata_code' : self.origin_airport.iata_code,
                'icao_code' : self.origin_airport.icao_code,
                'airport_type' : self.origin_airport.airport_type
            },

            "destination_airport" : {
                'airport_name' : self.destination_airport.airport_name,
                'airport_city' : self.destination_airport.airport_city,
                'airport_country' : self.destination_airport.airport_country, 
                'iata_code' : self.destination_airport.iata_code,
                'icao_code' : self.destination_airport.icao_code,
                'airport_type' : self.destination_airport.airport_type
            },
            
            "departure_date" : self.departure_date.strftime("%a , %d %b"),
            "departure_time" : self.departure_time.strftime("%H:%M"),
            "arrival_date" : self.arrival_date,
            "arrival_time" : self.arrival_time.strftime("%H:%M"),
            "flight_duration" : DateTime.strptime(str(self.arrival_date)+' '+str(self.arrival_time), FMT) - DateTime.strptime(str(self.departure_date)+' '+str(self.departure_time), FMT), # .strftime("%H hours %M minutes")
            "flight_price" : Fare.objects.get(flight=self).__getattribute__(seat_class),
        }

        if x == 1:
            del data['flight_price']
            x = 0
        return data



    def maximum_amount(self):
        seat = self.seat_config
        fare = Fare.objects.get(flight=self, seat=seat)
        max_eco = seat.economy_seats * fare.economy_fare
        max_bus = seat.business_seats * fare.business_fare
        max_fir = seat.first_seats * fare.first_fare

        return max_eco + max_bus + max_fir

    def current_amount(self):
        total = Payment.objects.filter(flight=self, status=True).aggregate(Sum('amount'))['amount__sum']
        return total


    def seats_left(self):
        bookings = Booking.objects.filter(flight=self, confirmed=True).count()
        data = {
            "total" : self.seat_config.total_seats - bookings,
            "economy" : self.seat_config.economy_seats - Booking.objects.filter(flight=self, seat_type="Economy", confirmed=True).count(),
            "business" : self.seat_config.business_seats - Booking.objects.filter(flight=self, seat_type="Business", confirmed=True).count(),
            "first" : self.seat_config.first_seats - Booking.objects.filter(flight=self, seat_type="First", confirmed=True).count()
        }
        return data    

    def flight_booked_percentage(self):
        return int( (Booking.objects.filter(flight=self, confirmed=True).count() / self.seat_config.total_seats ) * 100)

    def get_flight_deatils(self):
        fare = Fare.objects.get(flight=self, seat=self.seat_config)
        data = {
            "flight_information" : self.search_flight_result('all'),
            "seat_information" : {
                "default" : {
                    "total" : self.seat_config.total_seats,
                    "economy" :self.seat_config.economy_seats ,
                    "business" : self.seat_config.business_seats,
                    "first" : self.seat_config.first_seats
                },
                "available" : self.seats_left(),
                "booked" : {
                    "economy" : Booking.objects.filter(flight=self, seat_type="Economy", confirmed=True).count(),
                    "business" : Booking.objects.filter(flight=self, seat_type="Business", confirmed=True).count(),
                    "first" : Booking.objects.filter(flight=self, seat_type="First", confirmed=True).count()
                }
            },
            "pricing" : {
                "economy" : fare.economy_fare,
                "business" : fare.business_fare,
                "first" : fare.first_fare,
            }
        }
        return data    


    def __str__(self) -> str:
        return self.flight_number


class Seat(models.Model):
    flight = models.OneToOneField(Flight, models.CASCADE, related_name="seat_config")

    total_seats = models.PositiveSmallIntegerField(default=160)
    economy_seats = models.PositiveSmallIntegerField(null=True, default=0, blank=True) # 62.5%
    business_seats = models.PositiveSmallIntegerField(null=True, blank=True, default=0) # 28.125%
    first_seats = models.PositiveSmallIntegerField(null=True, blank=True, default=0) # 9.375%

    def __str__(self) -> str:
        return self.flight.flight_number


class Fare(models.Model):
    flight = models.ForeignKey(Flight, models.CASCADE, related_name="flight_fare")
    seat = models.ForeignKey(Seat, models.CASCADE, related_name="seat_fare")
    economy_fare = models.FloatField()
    business_fare = models.FloatField()
    first_fare = models.FloatField()

    def __str__(self) -> str:
        return self.flight.flight_number


class Profile(BaseModel):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=8, null=True, blank=True)
    passport_number = models.CharField(max_length=8, null=True, blank=True)
    citizenship = models.CharField(max_length=16, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)

    profile_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name


class Booking(BaseModel):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="booking_user")
    flight = models.ForeignKey(Flight, models.CASCADE, related_name="flight_booking")

    person_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=8)
    passport_number = models.CharField(max_length=8)
    citizenship = models.CharField(max_length=16)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=25, null=True, blank=True)

    pnr_code = models.CharField(default="Not Yet", max_length=8)
    seat_type = models.CharField(max_length=8)
    fare_amount = models.FloatField(null=True, blank=True)
    fare = models.ForeignKey(Fare, on_delete=models.CASCADE, related_name="fare_boooking", null=True, blank=True)

    confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.pnr_code + " (" + self.flight.flight_number + ")"


class Payment(models.Model):
    
    payment_id = models.CharField(default=get_random_string(10), unique=True, max_length=32)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="payment_user")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payment_booking")
    flight = models.ForeignKey(Flight, models.CASCADE, related_name="payment_flight")

    amount = models.FloatField()
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return self.payment_id

