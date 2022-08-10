from django.views import View
from django.shortcuts import render, redirect
from carts.models import Cart, CartItem


class CustomerCartView(View):
    def get(self, request):
        # Query existing cart or create new cart.
        # Used to query cart item in the code below.
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user_id=request.user.id)

        cart_items = CartItem.objects.filter(cart_id=cart.id)

        # Loop all cart item and calculate the total payable amount.
        total_amount = 0
        for cart_item in cart_items:
            total_amount = total_amount + cart_item.product.price * cart_item.quantity

        return render(request, 'c_cart_view.html', {'cart_items': cart_items, 'total_amount': total_amount})


class CustomerCheckoutView(View):
    def get(self, reqeust):
        return render(reqeust, 'c_checkout_view.html')