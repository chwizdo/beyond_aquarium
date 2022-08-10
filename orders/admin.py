from django.contrib import admin

from orders.models import Address, Order, OrderItem

admin.site.register(Order)
admin.site.register(Address)
admin.site.register(OrderItem)