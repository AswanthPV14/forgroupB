from django.contrib import admin
from .models import ServiceRequest, Customer, Booking

admin.site.register(Customer)
admin.site.register(ServiceRequest)
admin.site.register(Booking)
