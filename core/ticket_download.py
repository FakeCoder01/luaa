from django.http import FileResponse, HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from .models import Booking, Payment
import io, logging
from reportlab.pdfgen import canvas
from datetime import datetime as DateTime
from datetime import datetime

logger = logging.getLogger(__name__)

@login_required(login_url="/login")
def view_ticket(request, booking_id):
    try:
        if request.user.is_staff or request.user.is_superuser :
            if Booking.objects.filter(uid=booking_id).exists():
                booking = Booking.objects.get(uid=booking_id)
            else:
                return HttpResponseNotFound("Not found")
        elif Booking.objects.filter(uid=booking_id, profile=request.user.userprofile).exists():
            profile = request.user.userprofile
            booking = Booking.objects.get(uid=booking_id, profile=profile)
        else:
            return HttpResponseNotFound("Not found")
        
        
        payment = Payment.objects.get(booking=booking, status=True)
        
        flight = booking.flight
        FMT = "%Y-%m-%d %H:%M:%S"
        ticket = f"""\n
                \nFLIGHT TICKET\n
                --------------\n
                # Flight Information\n
                    Flight Number   :   {str(flight.flight_number).upper()}          ||        Luaa Airways\n
                    Flight Duration :   {DateTime.strptime(str(flight.arrival_date)+' '+str(flight.arrival_time), FMT) - DateTime.strptime(str(flight.departure_date)+' '+str(flight.departure_time), FMT)} H:M:S\n
                    Departure       :   {flight.departure_date.strftime("%d %B %Y")}, {flight.departure_time}\n
                    Origin Airport  :   {flight.origin_airport}\n
                    City, Country   :   {flight.origin_airport.airport_city}, {flight.origin_airport.airport_country}\n
                    Arrival         :   {flight.arrival_date.strftime("%d %B %Y")}, {flight.arrival_time}\n
                    Destination Airport :   {flight.destination_airport}\n
                    City, Country   :   {flight.destination_airport.airport_city}, {flight.destination_airport.airport_country}\n
                \n
                # Passenger Information\n
                    Full Name      :   {booking.person_name}\n
                    Sex            :   {booking.gender}      ,   Citizenship   :   {booking.citizenship}\n
                    Passport No.   :   {booking.passport_number}\n
                    Email Address  :   {booking.email} \n
                    Mobile No.     :   {booking.mobile_number}\n
                \n
                # Booking Information\n
                    PNR Code       :   {str(booking.pnr_code).upper()}\n   
                    Seating Class  :   {str(booking.seat_type).upper()}\n
                    Ticket Price   :   INR {booking.fare_amount}\n
                    Booked at      :   {booking.created_at.strftime("%d/%m/%Y %H:%M:%S")}\n
                \n
                # Payment Information\n
                    Total Amount   :   {payment.amount}\n
                    Staus          :   {'Paid' if payment.status else 'Awaiting'}\n
                    Payment ID     :   {payment.payment_id}\n
                    Payment Time   :   {payment.created_at.strftime("%d/%m/%Y %H:%M:%S")}\n     
                \n\n\n\n
                -- downloaded on {datetime.now().strftime("%d %B %Y %H:%M:%S")}
        """

        buffer = io.BytesIO()
        x = canvas.Canvas(buffer)
        x.setFontSize(size=13, leading=12)
        x.drawImage(x=250, y=380, image="static/images/logo/logo-icon-without-bg.png", mask='auto')
        ticket_object = x.beginText(75, 800)
        ticket_object.textLines(ticket)
        x.drawText(ticket_object)
        x.save()
        buffer.seek(0)

        pdf_filename = str(booking.pnr_code).upper() + "_" + str(booking.person_name).replace(" ", "_") + ".pdf"
        return FileResponse(buffer, as_attachment=True, filename=pdf_filename)
    except Exception as err:
        logger.error(err)
        return HttpResponseServerError("Something went wrong")