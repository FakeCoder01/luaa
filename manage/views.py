from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
import logging
from django.shortcuts import redirect, render
from core.models import *


# Create your views here.

logger = logging.getLogger(__name__)

def flight_formating(flight : Flight):
    try:
        current_amount = flight.current_amount()
        data = {
            "uid" : flight.uid,
            "flight_number" : flight.flight_number,
            "current_amount" :  0 if not current_amount else current_amount,
            "percentage_booked" : flight.flight_booked_percentage()
        }
        return data
    except Exception as err:
        logger.error(err)


@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def homePage(request):
    try:
        last_five_flights_details = [ flight_formating(x) for x in Flight.objects.all().order_by('-updated_at')[:5] ]
        context = {
            "last_five_flights_details" : last_five_flights_details,
            "last_five_payments" : Payment.objects.filter().order_by('-updated_at')[:5],
            "last_five_bookings" : Booking.objects.filter(confirmed=True).order_by('-created_at')[:8],
            "total_flights_booked" : Booking.objects.filter(confirmed=True).count(),
            "total_amount" : Payment.objects.filter(status=True).aggregate(Sum('amount'))['amount__sum'],
            "total_flights" : Flight.objects.all().count(),
            "total_users" : Profile.objects.all().count()
        }
        return render(request, "manage/home-page.html", context)

    except Exception as err:
        logger.error(err)

### All Flights
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage')
def all_flights(request):
    try:
        context = {
            "flights" : Flight.objects.all()
        }
        return render(request, 'manage/flights/all-flights.html', context)
    except Exception as err:
        logger.error(err)

### Add a new flight
@login_required(login_url='/manage/login/')    
@staff_member_required(login_url='/manage')
def add_flight(request):
    try:
        if request.method == 'POST':
            try :
                origin = str(request.POST['origin'])
                destination = str(request.POST['destination'])
                flight_number = request.POST['flight_number']

                departure_date = request.POST['departure_date']
                departure_time = request.POST['departure_time']
                arrival_date = request.POST['arrival_date']
                arrival_time = request.POST['arrival_time']

                total_seats = int(request.POST['total_seats'])
                economy_seats = int(request.POST['economy_seats'])
                business_seats = int(request.POST['business_seats'])
                first_seats = int(request.POST['first_seats'])

                economy_fare = request.POST['economy_fare']
                business_fare = request.POST['business_fare']
                first_fare = request.POST['first_fare']
                
                if total_seats != (economy_seats + business_seats + first_seats):
                    messages.error(request, "Seat configaration is not valid")
                    return redirect('/manage/flights/add?error=True')

                if origin.upper() == destination.upper():
                    messages.error(request, "Origin and Destination have to be different")
                    return redirect('/manage/flights/add?error=True')

                if not Airport.objects.filter(iata_code=origin).exists():
                    messages.error(request, "Origin Airport Invalid")
                    return redirect('/manage/flights/add?error=True')

                if not Airport.objects.filter(iata_code=destination).exists():
                    messages.error(request, "Destination Airport invalid")
                    return redirect('/manage/flights/add?error=True') 

                if departure_date > arrival_date:
                    messages.error(request, "Arrival date have to be same or after Departure date")
                    return redirect('/manage/flights/add?error=True')  

                if departure_date == arrival_date and departure_time > arrival_time:
                    messages.error(request, "Arrival time have to be after Departure time")
                    return redirect('/manage/flights/add?error=True')      

                new_flight = Flight.objects.create(
                    flight_number = flight_number,
                    origin_airport = Airport.objects.get(iata_code=origin),
                    destination_airport = Airport.objects.get(iata_code=destination),
                    departure_date = departure_date,
                    departure_time = departure_time,
                    arrival_date = arrival_date,
                    arrival_time = arrival_time

                )
                new_seat_config = Seat.objects.create(
                    flight = new_flight,
                    total_seats = total_seats,
                    economy_seats = economy_seats,
                    business_seats = business_seats,
                    first_seats = first_seats
                ) 
                new_fare = Fare.objects.create(
                    flight = new_flight,
                    seat = new_seat_config,
                    economy_fare = economy_fare,
                    business_fare = business_fare,
                    first_fare = first_fare
                )
                messages.success(request, "Flight has been added")
                return redirect(f"/manage/flights/{new_flight.uid}?add=True")
            except Exception as err:
                logger.error(err)
                return redirect('/manage/flights/add')

        context = {
            "airports" : Airport.objects.all()
        }
        return render(request, 'manage/flights/add-flight.html', context)
    except Exception as err:
        logger.error(err)


# Get details of a flight
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def flight_details(request, flight_id):
    try:
        if Flight.objects.filter(uid=flight_id).exists():
            flight = Flight.objects.get(uid=flight_id)
            context = {
                "flight" : flight,
                "bookings" : Booking.objects.filter(flight=flight),
                "all" : flight.get_flight_deatils(),
                "income" : {
                    "max" : flight.maximum_amount(),
                    "current" : flight.current_amount()
                }
            }

            return render(request, 'manage/flights/flight-details.html', context)
        logger.info(msg="Invalid Flight ID")
        return HttpResponse("404 Not found")   
    except Exception as err:
        logger.error(err)


### Edit a flight
@login_required(login_url='/manage/login/')    
@staff_member_required(login_url='/manage')
def edit_flight(request, flight_id):
    try:
        if Flight.objects.filter(uid=flight_id).exists():
            flight = Flight.objects.get(uid=flight_id)
            if request.method == 'POST':
                try :
                    origin = str(request.POST['origin'])
                    destination = str(request.POST['destination'])
                    flight_number = request.POST['flight_number']

                    departure_date = request.POST['departure_date']
                    departure_time = request.POST['departure_time']
                    arrival_date = request.POST['arrival_date']
                    arrival_time = request.POST['arrival_time']

                    total_seats = int(request.POST['total_seats'])
                    economy_seats = int(request.POST['economy_seats'])
                    business_seats = int(request.POST['business_seats'])
                    first_seats = int(request.POST['first_seats'])

                    economy_fare = request.POST['economy_fare']
                    business_fare = request.POST['business_fare']
                    first_fare = request.POST['first_fare']
                    
                    if total_seats != (economy_seats + business_seats + first_seats):
                        messages.error(request, "Seat configaration is not valid")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True')

                    if origin.upper() == destination.upper():
                        messages.error(request, "Origin and Destination have to be different")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True')

                    if not Airport.objects.filter(iata_code=origin).exists():
                        messages.error(request, "Origin Airport Invalid")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True')

                    if not Airport.objects.filter(iata_code=destination).exists():
                        messages.error(request, "Destination Airport invalid")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True') 

                    if departure_date > arrival_date:
                        messages.error(request, "Arrival date have to be same or after Departure date")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True')  

                    if departure_date == arrival_date and departure_time > arrival_time:
                        messages.error(request, "Arrival time have to be after Departure time")
                        return redirect(f'/manage/flights/{flight_id}/change?error=True') 

                    flight.flight_number = flight_number
                    flight.origin_airport = Airport.objects.get(iata_code=origin)
                    flight.destination_airport = Airport.objects.get(iata_code=destination)
                    flight.departure_date = departure_date
                    flight.departure_time = departure_time
                    flight.arrival_date = arrival_date
                    flight.arrival_time = arrival_time
                    flight.save()

                    seat = Seat.objects.get(flight=flight)
                    seat.total_seats = total_seats
                    seat.economy_seats = economy_seats
                    seat.business_seats = business_seats
                    seat.first_seats = first_seats
                    seat.save()

                    fare = Fare.objects.get(flight=flight, seat=seat)
                    fare.economy_fare = economy_fare
                    fare.business_fare = business_fare
                    fare.first_fare = first_fare
                    fare.save()
    
                    messages.success(request, "Flight has been updated")
                    return redirect(f"/manage/flights/{flight_id}?updated=True")
                except Exception as err:
                    logger.info(err)
                    return redirect(f"/manage/flights/{flight.uid}?error=True")
                
            context = {
                "flight" : flight,
                "airports" : Airport.objects.all(),
                "fare" : Fare.objects.get(flight=flight)
            }
            return render(request, 'manage/flights/edit-flight.html', context)
        logger.info(msg="Invalid Flight ID")
        return HttpResponse("404 Not found")   
    except Exception as err:
        logger.error(err)


### Delete a flight
@login_required(login_url='/manage/login/')    
@staff_member_required(login_url='/manage')
def delete_flight(request, flight_id):
    pass



### All bookings of a particular flight
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage')
def flight_tickets(request, flight_id):
    pass 


### All tickets
@login_required(login_url='/manage/login/')    
@staff_member_required(login_url='/manage/login')
def all_tickets(request):
    try:
        context = {
            "bookings" : Booking.objects.filter(confirmed=True),
        }
        return render(request, 'manage/tickets/all-tickets.html', context)
    except Exception as err:
        logger.error(err)


### Details of a partucular ticket
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def ticket_details(request, booking_id):
    try:
        if Booking.objects.filter(uid=booking_id).exists():
            booking = Booking.objects.get(uid=booking_id)

            if request.GET.get('rdr', None) == "PAYMENT" and request.GET.get('payment_id', None) != None:
                p_id = request.GET.get('payment_id')
                pymt = Payment.objects.filter(booking=booking, payment_id=p_id)

                if len(pymt) != 1:
                    return HttpResponse("Wrong Payment ID")
                
                pymt = pymt[0]

            else:
                pymt = Payment.objects.get(booking=booking, status=True)

            context = {
                "booking" : booking,
                "payment" : pymt,
            }
            return render(request, 'manage/tickets/ticket-details.html', context)
        logger.info(msg="Booking doesn't exist")
        return HttpResponseNotFound()
    except Exception as err:
        logger.error(err)
        return HttpResponse("No ticket")
    
### Edit a ticket
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def edit_ticket(request, ticket_id):
    try:
        if Booking.objects.filter(uid=ticket_id).exists():
            ticket = Booking.objects.get(uid=ticket_id)
            context = {
                "ticket_details" : ticket
            }
            if request.method == 'POST':
                pass
            return render(request, 'manage/tickets/edit-ticket.html', context)
        logger.info(msg="Booking not found")
        return HttpResponseNotFound()
    except Exception as err:
        logger.error(err)

### All users
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def all_users(request):
    try:
        context = {
            "profiles" : Profile.objects.all()
        }
        return render(request, 'manage/users/all-users.html', context)
    except Exception as err:
        logger.error(err)

### Details of a user
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def user_details(request, userid):
    try:
        if Profile.objects.filter(uid=userid).exists():
            context = {
                "user_details" : Profile.objects.get(uid=userid)
            }
            return render(request, 'manage/users/user-details.html', context)
        logger.info(msg="User not found")
        return HttpResponseNotFound()
    except Exception as err:
        logger.error(err)

### Edit a user
@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def edit_user(request, userid):
    try:
        if Profile.objects.filter(uid=userid).exists():
            profile = Profile.objects.get(uid=userid)
            context = {
                "user_details" : profile
            }
            if request.method == 'POST':
                try:
                    # personal information
                    first_name = request.POST['first_name']
                    last_name = request.POST['last_name']
                    gender = request.POST['gender']
                    citizenship = request.POST['citizenship']
                    passport_number = request.POST['passport_number']
                    profile_active = False
                    if 'profile_active' in request.POST and request.POST['profile_active'] == '1':
                        profile_active = True
                    # contact information
                    mobile_number = request.POST['mobile_number']
                    email = str(request.POST['email']).replace(' ', '')

                    # account information
                    username = str(request.POST['username']).replace(' ', '')
                    form_userid = request.POST['userid']
                    password = request.POST['password']
                    confirm_password = request.POST['confirm_password']


                    full_name = first_name + " " + last_name
                    user = profile.user
                        
                    # declaration : consiousness check

                    if 'declaration' in request.POST and request.POST['declaration'] == '1':

                        if username != user.username and User.objects.filter(username=username).exists():
                            messages.error(request, "Username already taken")
                            return redirect(f'/manage/users/{userid}/change?res=username-taken')
                        else:
                            user.username = username
                            messages.success(request, "Username updated")

                        if email != user.email and User.objects.filter(email=email).exists():
                            messages.error(request, "Email already taken")
                            return redirect(f'/manage/users/{userid}/change?res=email-taken') 
                        else:
                            user.email = email
                            messages.success(request, "Email updated")

                        if password == '' or password == ' ':
                            pass 
                        elif password == confirm_password:
                            user.set_password(password)
                            messages.success(request, "Password changed")
                        else:
                            messages.error(request, " Password did not match")
                            return redirect(f'/manage/users/{userid}/change?res=password-mismatch') 

                        if user.first_name != first_name:
                            user.first_name = first_name
                            messages.success(request, "Name updated")

                        if user.last_name != last_name:
                            user.last_name = last_name
                            messages.success(request, "Name updated")

                        profile.full_name = full_name

                        if profile.gender != gender:
                            profile.gender = gender
                            messages.success(request, "Gender updated")

                        if profile.passport_number != str(passport_number).upper():
                            profile.passport_number = str(passport_number).upper()
                            messages.success(request, "Passport number updated")

                        if profile.citizenship != str(citizenship).upper():
                            profile.citizenship = str(citizenship).upper()
                            messages.success(request, "Citizenship updated")

                        if profile.mobile_number != mobile_number:
                            profile.mobile_number = mobile_number
                            messages.success(request, "Mobile number updated")

                        if profile.profile_active != profile_active:
                            profile.profile_active = profile_active
                            messages.success(request, "Profile status updated")

                        profile.save()
                        user.save()    
                        messages.success(request, "Profile updated")    
                        return redirect(f"/manage/users/{userid}/change?res=True")
                    return redirect(f"/manage/users/{userid}/change?res=not-declared")    
                except Exception as err:
                    logger.error(err)
                    messages.error(request, "Something went wrong")
                    return redirect(f"/manage/users/{userid}/change?res=err") 
            return render(request, 'manage/users/edit-user.html', context)
        logger.info(msg="Invalid Userid")
        return redirect('/manage/users/?res=userid-invalid')
    except Exception as err:
        logger.error(err)


def loginManager(request):
    try:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_staff or user.is_superuser:
                # User is authenticated
                login(request, user)
                messages.success(request, "Login successful")
                return redirect(f'/manage/?login=true')
            messages.error(request, "Invalid credentials")        
            return redirect("/manage/login?msg=invalid credentials")    
        return render(request, 'manage/login.html', {"page_title" : "Login to Luua"})
    except Exception as err:
        logger.error(err)


def logoutManager(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/manage')


@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def all_airports(request):
    try:
        context = {
            "airports" : Airport.objects.all()
        }
        return render(request, 'manage/airports/all-airports.html', context)
    except Exception as err:
        logger.error(err)

@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def add_airports(request):
    try:
        if request.method == 'POST':
            try :
                airport_name = request.POST['airport_name']
                airport_city = request.POST['airport_city']
                iata_code = request.POST['iata_code']
                icao_code = request.POST['icao_code']
                airport_country = request.POST['airport_country']
                airport_type = request.POST['airport_type']

                if Airport.objects.filter(iata_code=iata_code).exists():
                    messages.error(request, "IATA code of an Airport already exists")
                    return redirect('/manage/airports/add?error=True')

                if Airport.objects.filter(icao_code=icao_code).exists():
                    messages.error(request, "ICAO code of an Airport already exists")
                    return redirect('/manage/airports/add?error=True') 

                if Airport.objects.filter(airport_name=airport_name).exists():
                    messages.error(request, "Airport name already exists")
                    return redirect('/manage/airports/add?error=True') 
        

                new_airport = Airport.objects.create(

                    airport_name = airport_name,
                    airport_city = airport_city,
                    iata_code = iata_code.upper(),
                    icao_code = icao_code.upper(),
                    airport_country = airport_country,
                    airport_type = airport_type
                )
                
                messages.success(request, "Airport has been added")
                return redirect(f"/manage/airports/?add=True&airport_id={new_airport.uid}")

            except Exception as err:
                logger.error(err)
                messages.error(request, "Something went wrong")
                return redirect('/manage/airports/add?error=True')

        return render(request, 'manage/airports/add-airport.html')
    except Exception as err:
        logger.error(err)

@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def airport_details(request, airport_id):
    try:
        if Airport.objects.filter(uid=airport_id).exists():
            airport = Airport.objects.get(uid=airport_id)
            context = {
                "flights" : Flight.objects.filter(Q(origin_airport=airport) | Q(destination_airport=airport)),
                "airport" : airport,
            }
            return render(request, 'manage/airports/airport-details.html', context)
        logger.info(msg="Invalid Airport ID")
        return HttpResponse("404 Not found") 
    except Exception as err:
        logger.error(err)


@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def edit_airport(request, airport_id):
    try:
        if Airport.objects.filter(uid=airport_id).exists():
            airport = Airport.objects.get(uid=airport_id)
            if request.method == 'POST':
                try :
                    airport_name = request.POST['airport_name']
                    airport_city = request.POST['airport_city']
                    iata_code = request.POST['iata_code']
                    icao_code = request.POST['icao_code']
                    airport_country = request.POST['airport_country']
                    airport_type = request.POST['airport_type']

                    airport.airport_name = airport_name
                    airport.airport_city = airport_city
                    airport.iata_code = iata_code.upper()
                    airport.icao_code = icao_code.upper()
                    airport.airport_country = airport_country
                    airport.airport_type = airport_type
                    airport.save()

    
                    messages.success(request, "Airport has been updated")
                    return redirect(f"/manage/airports/{airport.uid}?updated=True")
                except Exception as err:
                    print(err)
                    return redirect(f"/manage/airports/{airport.uid}?error=True")
                
            context = {
                "airport" : airport,
            }
            return render(request, 'manage/airports/edit-airport.html', context)
        logger.info(msg="Invalid Airport ID")
        return HttpResponse("404 Not found") 
    except Exception as err:
        logger.error(err)


@login_required(login_url='/manage/login')    
@staff_member_required(login_url='/manage/login')
def all_payments(request):    
    try:
        context = {
            "payments" : Payment.objects.all()
        }
        return render(request, 'manage/payments/all-payments.html', context)
    except Exception as err:
        logger.error(err)