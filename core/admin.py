from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Fare)
admin.site.register(Profile)
admin.site.register(Booking)
admin.site.register(Payment)

