from django.contrib import admin

from orders.models import Address, Order

admin.site.register(Order)
admin.site.register(Address)