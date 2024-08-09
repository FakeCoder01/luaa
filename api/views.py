from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from core.models import Flight, Airport
from .serializers import SearchFlightSerializer
from django.db.models import Q
import logging
# Create your views here.


logger = logging.getLogger(__name__)

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'search_airports': '/api/search/airports/',
        'search_flights': '/api/search/flights/',
    }
    return Response(api_urls)

def ConnectingFlight(origin, destination, seat_class, departure_date, departure_time=None):
    try:
        origin_flights = []
        if departure_time is not None:
            print("Hit1")
            origin_flights = Flight.objects.filter(origin_airport=origin, departure_date=departure_date, departure_time=departure_time)
        else:
            origin_flights = Flight.objects.filter(origin_airport=origin, departure_date=departure_date)

        destination_flights = Flight.objects.filter(destination_airport=destination)
        connecting_flights1 = Flight.objects.filter(origin_airport__in=origin_flights.values('origin_airport'), departure_time=departure_time)
        connecting_flights2 = Flight.objects.filter(destination_airport__in=destination_flights.values('destination_airport'))
        connecting_flights = connecting_flights1.union(connecting_flights2)
        
        final_list = []
        for flight1 in origin_flights:
            for flight2 in connecting_flights:
                if flight1.destination_airport == flight2.origin_airport:
                    x = flight1.search_flight_result(seat_class)
                    y = flight2.search_flight_result(seat_class)

                    final_list.append(
                        {
                            "first_flight" : x,
                            "final_flight" : y,
                            "flight_price" : x['flight_price'] + y['flight_price'],
                            "flight_duration" : x['flight_duration'] + y['flight_duration']
                        }
                    )
    
        for flight1 in connecting_flights:
            for flight2 in destination_flights:
                if flight1.destination_airport == flight2.origin_airport:
                    x = flight1.search_flight_result(seat_class)
                    y = flight2.search_flight_result(seat_class)
                    final_list.append(
                        {
                            "first_flight" : x,
                            "final_flight" : y,
                            "flight_price" : x['flight_price'] + y['flight_price'],
                            "flight_duration" : x['flight_duration'] + y['flight_duration'],
                        }
                    )
        
        return final_list
    except Exception as err:
        logging.error(err)
        return False


@api_view(['GET'])
def SearchFlight(request):
    try:
        search_params = SearchFlightSerializer(data=request.GET or None)
        if search_params.is_valid():
            seat_class = request.GET['seat_class']
            origin = request.GET['origin']
            destination = request.GET['destination']
            departure_date = request.GET['departure_date']

            if not Airport.objects.filter(iata_code=origin.upper()).exists():
                return Response({"error":"origin not valid"})
            if not Airport.objects.filter(iata_code=destination.upper()).exists():
                return Response({"error":"destination not valid"})

            origin = Airport.objects.get(iata_code=origin.upper())
            destination = Airport.objects.get(iata_code=destination.upper())

            
            
            flights = []
            connecting_flights = []
            if 'flight_type' in request.GET and request.GET['flight_type'] == "connecting":

                if request.GET.get('departure_time', '') != '':
                    departure_time = request.GET['departure_time']
                    connecting_flights = ConnectingFlight(origin, destination, seat_class, departure_date, departure_time)
                else:
                    connecting_flights  = ConnectingFlight(origin, destination, seat_class, departure_date)


            elif 'flight_type' in request.GET and request.GET['flight_type'] == "all":
                if request.GET.get('departure_time', '') != '':
                    print("Hit2")
                    departure_time = request.GET['departure_time']
                    print(departure_time)
                    flights = [ 
                        x.search_flight_result(seat_class) for x in 
                        Flight.objects.filter(origin_airport=origin, destination_airport=destination, departure_date=departure_date, departure_time=departure_time) 
                    ]
                    connecting_flights = ConnectingFlight(origin, destination, seat_class, departure_date, departure_time)
                else:
                    flights = [ 
                        x.search_flight_result(seat_class) for x in 
                        Flight.objects.filter(origin_airport=origin, destination_airport=destination, departure_date=departure_date) 
                    ]
                    connecting_flights = ConnectingFlight(origin, destination, seat_class, departure_date)
            else:
                if request.GET.get('departure_time', '') != '':
                    departure_time = request.GET['departure_time']
                    flights = [ 
                        x.search_flight_result(seat_class) for x in 
                        Flight.objects.filter(origin_airport=origin, destination_airport=destination, departure_date=departure_date, departure_time=departure_time)
                    ]
                else:
                    flights = [ x.search_flight_result(seat_class) for x in Flight.objects.filter(origin_airport=origin, destination_airport=destination, departure_date=departure_date) ]

            sort_key = ''
            if 'sort_key' in request.GET and request.GET['sort_key'] != '':
                sort_key = request.GET['sort_key']

            if sort_key == 'price':
                flights = sorted(flights, key=lambda k: k['flight_price'])
                connecting_flights = sorted(connecting_flights, key=lambda k: k['flight_price'])

            elif sort_key == 'time':
                flights = sorted(flights, key=lambda k: k['flight_duration'])
                connecting_flights = sorted(connecting_flights, key=lambda k: k['flight_duration'])

            elif sort_key == 'stops':
                flights = flights
                
            else:
                flights = flights

            payload = {
                "status_code" : 200,
                "flights_found" : len(flights) + len(connecting_flights),
                "seat_class" : seat_class,
                "flights" : flights,
                "connecting_flights" : connecting_flights,
            }
            return Response(payload)
        logger.info(msg="Invalid serializer")
        return Response({"error":"not valid"})
    except Exception as err:
        logging.error(err)
        return Response(status=500)


@api_view(['GET'])
def AirportFillUp(request):
    try:
        airports = Airport.objects.all().defer("created_at", "updated_at").values()
        if 'airport_search' in request.GET and request.GET['airport_search'] != '':
            airport_search = request.GET['airport_search']
            airports = Airport.objects.filter(
                Q(airport_name__icontains=airport_search) |
                Q(airport_city__icontains=airport_search) |
                Q(airport_country__icontains=airport_search) |
                Q(iata_code__icontains=airport_search) |
                Q(icao_code__icontains=airport_search) 
            ).defer("created_at", "updated_at").values()

        return Response({"airports":airports})      
    except Exception as err:
        logger.error(err)