from django.views import View
from django.shortcuts import render, redirect

from orders.models import Address, Order, OrderItem

from carts.models import Cart, CartItem
from utils.views import Util


class CustomerOrderView(View):
    def get(self, request):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        orders = Order.objects.filter(user_id=request.user.id)

        return render(request, 'c_order_view.html', {'orders': orders})

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

        shipping = request.POST.get('shipping')
        remark = request.POST.get('remark')

        order = Order.objects.create(
            user_id=request.user.id,
            name=name, 
            email=email, 
            phone=phone,
            shipping=shipping,
            remark=remark
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

        orders = Order.objects.filter(user_id=request.user.id)

        return render(request, 'c_order_view.html', {'orders': orders})

    
class CustomerOrderDetailView(View):
    def get(self, request, order_id):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        # If product id is not present in the path parameter,
        # redirect user back to product listing page.
        if order_id is None:
            return redirect('c_order')

        # Query product object from product id in path parameter,
        # if product object is not found, redirect user back to product listing page.
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return redirect('c_order')

        order_items = OrderItem.objects.filter(order_id=order_id)

        # Loop all cart item and calculate the total payable amount.
        total_amount = 0
        for order_item in order_items:
            total_amount = total_amount + order_item.price * order_item.quantity

        address = Address.objects.get(order_id=order.id)

        return render(request, 'c_order_detail_view.html', {'order': order, 'order_items': order_items, 'total_amount': total_amount, 'address': address})


class AdminOrderView(View):
    def get(self, request):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        orders = Order.objects.all()

        return render(request, 'a_order_view.html', {'orders': orders})


class AdminOrderDetailView(View):
    def get(self, request, order_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If product id is not present in the path parameter,
        # redirect user back to product listing page.
        if order_id is None:
            return redirect('a_order')

        # Query product object from product id in path parameter,
        # if product object is not found, redirect user back to product listing page.
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return redirect('a_order')

        order_items = OrderItem.objects.filter(order_id=order_id)

        # Loop all cart item and calculate the total payable amount.
        total_amount = 0
        for order_item in order_items:
            total_amount = total_amount + order_item.price * order_item.quantity
        
        address = Address.objects.get(order_id=order.id)

        return render(request, 'a_order_detail_view.html', {'order': order, 'order_items': order_items, 'total_amount': total_amount, 'address': address})

    def post(self, request, order_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If order id is not present in the path parameter,
        # redirect user back to order listing page.
        if order_id is None:
            return redirect('a_order')

        # Query order object from order id in path parameter,
        # if order object is not found, redirect user back to order listing page.
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return redirect('a_order')

        order_items = OrderItem.objects.filter(order_id=order_id)

        # Loop all order item and calculate the total payable amount.
        total_amount = 0
        for order_item in order_items:
            total_amount = total_amount + order_item.price * order_item.quantity

        # if more than one address is retrieved, cancel the operation.
        try:
            address = Address.objects.get(order_id=order_id)
        except:
            return render(request, 'a_order_detail_view.html', {'order': order, 'order_items': order_items, 'total_amount': total_amount, 'address': address})

        method = request.POST.get('_method')

        if method == 'PUT':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            street = request.POST.get('street')
            city = request.POST.get('city')
            postcode = request.POST.get('postcode')
            state = request.POST.get('state')
            country = request.POST.get('country')

            shipping = request.POST.get('shipping')
            remark = request.POST.get('remark')

            order.name = name
            order.email = email
            order.phone = phone
            order.shipping = shipping
            order.remark = remark
            order.save()

            address.street = street
            address.city = city
            address.postcode = postcode
            address.state = state
            address.country = country
            address.save()

        return render(request, 'a_order_detail_view.html', {'order': order, 'order_items': order_items, 'total_amount': total_amount, 'address': address})

            


