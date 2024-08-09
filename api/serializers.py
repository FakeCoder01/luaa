from rest_framework import serializers


class SearchFlightSerializer(serializers.Serializer):
    origin = serializers.CharField(max_length=50)
    destination = serializers.CharField(max_length=50)
    departure_date = serializers.DateTimeField()
    return_flight = serializers.BooleanField()
    seat_class = serializers.CharField(max_length=16)
    flight_type = serializers.CharField(max_length=16)


class AirportListSerializer(serializers.Serializer):

    airport_id = serializers.UUIDField()
    airport_name = serializers.CharField(max_length=200)
    airport_city = serializers.CharField(max_length=50)
    airport_country = serializers.CharField(max_length=16)
    iata_code = serializers.CharField(max_length=3)
    icao_code = serializers.CharField(max_length=4)
