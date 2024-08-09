from django.urls import path, include
from . import views
from . import chat
from .search import global_search, flight_admin_search_api



urlpatterns = [
    path('', views.homePage, name='homepage'),

    path('support/', include('chat.urls'), name="chat_support"),

    path('chat/<str:chat_id>/', chat.chat_room, name="chat_room"),

    path('flights/', views.all_flights, name="all_flights"), #
    path('flights/add/', views.add_flight, name="add_flight"),
    path('flights/<str:flight_id>/', views.flight_details, name="flight_details"),
    path('flights/<str:flight_id>/change/', views.edit_flight, name="edit_flight"),
    path('flights/<str:flight_id>/delete/', views.delete_flight, name="delete_flight"),
    path('flights/<str:flight_id>/bookings/', views.flight_tickets, name="flight_tickets"),

    path('tickets/', views.all_tickets, name="all_tickets"),
    path('tickets/<str:booking_id>/', views.ticket_details, name="ticket_details"),
    path('tickets/<str:booking_id>/change/', views.edit_ticket, name="edit_ticket"),

    path('users/', views.all_users, name="all_users"), #
    path('users/<str:userid>/', views.user_details, name="user_details"),
    path('users/<str:userid>/change/', views.edit_user, name="edit_user"),



    path('login/', views.loginManager, name="loginManager"),
    path('logout/', views.logoutManager, name="logoutManager"),

    path('airports/', views.all_airports, name="all_airports"),
    path('airports/add/', views.add_airports, name="add_airports"),
    path('airports/<str:airport_id>/', views.airport_details, name="airport_details"),
    path('airports/<str:airport_id>/change/', views.edit_airport, name="edit_airports"),

    
    path('payments/', views.all_payments, name="all_payments"),

    path('search/', global_search, name="search"),
    path('search/flights/', flight_admin_search_api, name="flight_admin_search_api"),

]