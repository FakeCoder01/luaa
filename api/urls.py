
from django.urls import path
from . import views
from .email_service import email_sent_many


urlpatterns = [
    path('', views.ApiOverview, name='api_routes'),
    path('search/flights/', views.SearchFlight, name="search_flights"),
    path('search/airports/', views.AirportFillUp, name="airport_fill_up"),
    path('email/many/', email_sent_many, name="email_sent_many"),
]