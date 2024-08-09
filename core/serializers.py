from rest_framework import serializers

from .models import Booking

class FlightBookingSerializer(serializers.Serializer):
    class Meta:
        model = Booking
        fields = ('person_name', 'gender', 'passport_number', 'citizenship', 'mobile_number', 'email', 'seat_type', 'fare_amount')
