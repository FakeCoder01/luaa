from django.urls import path, include
from . import views
from . import ticket_download
urlpatterns = [

    path('', views.homepage, name="homepage"),
    
    path('login/', views.login_user, name="login_user"),
    path('signup/', views.signup_user, name="signup_user"),
    path('logout/', views.logout_user, name="logout_user"),

    path('support/', include('chat.urls'), name="support"),

    path('profile/', views.manage_profile, name="manage_profile"),
    path('privacy-security/', views.privacy_security, name="privacy_security"),

    path('search/', views.search_flight, name="search_flight"),
    path('flight/<str:flight_id>/', views.flight_deatils, name="flight_deatils"),

    path('flight/<str:flight_id>/book/', views.fill_booking_details, name="fill_booking_details"),
    path('flight/<str:flight_id>/payment/<str:booking_id>/pay/', views.book_flight, name="payment_flight"),

    path('bookings/', views.bookings, name="bookings"),
    path('bookings/<str:booking_id>/', views.booking_details, name="booking_details"),
    path('bookings/<str:booking_id>/cancel/', views.cancel_flight, name="cancel_flight"),
    path('bookings/<str:booking_id>/change/', views.edit_booking, name="edit_booking"),

    path('tickets/<str:booking_id>/', ticket_download.view_ticket, name="view_ticket"),

    path('payments/', views.payments, name="payments"),
    path('payments/<str:payment_id>/', views.invoice_payment, name="invoice_payment"),

    path('paymenthandler/flight/', views.payment_handler, name="payment_handler"),
]