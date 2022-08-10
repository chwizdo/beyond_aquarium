from django.views import View
from django.shortcuts import render, redirect

from orders.models import Address, Order


class CustomerOrderView(View):
    def post(self, request):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        street = request.POST.get('street')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        state = request.POST.get('state')
        country = request.POST.get('country')

        order = Order.objects.create(name=name, email=email, phone=phone)
        address = Address.objects.create(street=street, city=city, postcode=postcode, state=state, country=country, order_id=order.id)

        return redirect('c_checkout')
