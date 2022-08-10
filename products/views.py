from django.views import View
from django.shortcuts import render, redirect
from carts.models import Cart, CartItem

from products.models import Product, ProductCategory

class CustomerProductView(View):
  def get(self, request, category_id = None):
    if not request.user.is_authenticated:
      return redirect('c_login')

    product_categories = ProductCategory.objects.all()

    try:
        if category_id is not None:
            ProductCategory.objects.get(id=category_id)
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.all()
    except ValueError and ProductCategory.DoesNotExist:
        products = Product.objects.all()
    
    return render(request, 'c_product_view.html', {'products': products, 'product_categories': product_categories})

class CustomerProductDetailView(View):
    def get(self, request, product_id = None):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')

        # If product id is not present in the path parameter,
        # redirect user back to product listing page.
        if product_id is None:
            return redirect('c_product')

        # Query product object from product id in path parameter,
        # if product object is not found, redirect user back to product listing page.
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('c_product')

        # Query existing cart or create new cart.
        # Used to query cart item in the code below.
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user_id=request.user.id)

        # Check if this item is already added to cart previously.
        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart_id=cart.id)
            quantity = cart_item.quantity
        except CartItem.DoesNotExist:
            quantity = None

        return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': quantity})

    def post(self, request, product_id = None):
        # Redirect user to login screen if user is unauthenticated.
        if not request.user.is_authenticated:
            return redirect('c_login')
        
        # If product id is not present in the path parameter,
        # redirect user back to product listing page.
        if product_id is None:
            return redirect('c_product')

        # Query product object from product id in path parameter,
        # if product object is not found, redirect user back to product listing page.
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('c_product')

        # Query existing cart or create new cart.
        # Used to query cart item in the code below.
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user_id=request.user.id)

        # Query cart item for create, update and delete operation below.
        # Value of cart item is None when it's not found.
        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart_id=cart.id)
            cart_item_quantity = cart_item.quantity
        except CartItem.DoesNotExist:
            cart_item = None
            cart_item_quantity = None

        method = request.POST.get('_method')

        if method == 'post':
            quantity = request.POST.get('quantity')

            # Check for invalid quantity input.
            invalid_input = False
            if quantity is None or int(quantity) > product.stock:
                invalid_input = True

            # Refresh the page if invalid quantity input.
            if invalid_input:
                return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': cart_item_quantity})

            if cart_item is not None:
                # Update quantity of the existing cart item.
                cart_item.quantity = quantity
                cart_item.save()
                return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': quantity})
            else:
                # Create a new cart item with the quantity input.
                CartItem.objects.create(product_id=product_id, quantity=quantity, cart_id=cart.id)
                return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': quantity})
        elif method == 'delete':
            if cart_item is not None:
                # Delete existing cart item
                cart_item.delete()
            return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': None})
        else:
            # Refresh the page if invalid form submission method.
            return render(request, 'c_product_detail_view.html', {'product': product, 'quantity': cart_item_quantity})
