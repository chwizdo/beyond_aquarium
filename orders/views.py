from django.views import View
from django.shortcuts import render, redirect

from orders.models import Address, Order, OrderItem

from carts.models import Cart, CartItem


class CustomerOrderView(View):
    def post(self, request):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        # Check if customer have an existing cart
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Cart.DoesNotExist:
            return redirect('c_cart')

        # Check if customer have any existing cart items
        cart_items = CartItem.objects.filter(cart_id=cart.id)
        if len(cart_items) < 1:
            return redirect('c_cart')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        street = request.POST.get('street')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        state = request.POST.get('state')
        country = request.POST.get('country')

        order = Order.objects.create(
            name=name, 
            email=email, 
            phone=phone
        )

        Address.objects.create(
            street=street, 
            city=city, 
            postcode=postcode, 
            state=state, 
            country=country, 
            order_id=order.id
        )
        
        for cart_item in cart_items:
            product = cart_item.product

            product.stock = product.stock - cart_item.quantity
            product.save()

            OrderItem.objects.create(
                name=product.name, 
                price=product.price, 
                description=product.description, 
                quantity=cart_item.quantity, 
                category=product.category.name, 
                order_id=order.id,
            )

            cart_item.delete()

        return redirect('c_checkout')
