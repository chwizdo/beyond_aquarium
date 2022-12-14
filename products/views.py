from unicodedata import name
from django.views import View
from django.shortcuts import render, redirect
from auths.models import Role
from carts.models import Cart, CartItem

from products.models import Product, ProductCategory
from utils.views import Util

class CustomerProductView(View):
    def get(self, request, category_id = None):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

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
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

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
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res
        
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


class APIProductView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        products = Product.objects.all()

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_product_view.html', {'products': products, 'role': role.role})


class APIProductDetailView(View):
    def get(self, request, product_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if product_id is None:
            return redirect('a_product')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('a_product')

        product_categories = ProductCategory.objects.all()

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_product_detail_view.html', {'product': product, 'product_categories': product_categories, 'role': role.role})
    def post(self, request, product_id):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        # If user id is not present in the path parameter,
        # redirect user back to user listing page.
        if product_id is None:
            return redirect('a_product')

        # Query user object from user id in path parameter,
        # if user object is not found, redirect user back to user listing page.
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('a_product')

        method = request.POST.get('_method')

        if method == 'PUT':
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')
            category = request.POST.get('category')

            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.image = image
            product.category_id = category
            product.save()
        if method == 'DELETE':
            product.delete()
            return redirect('a_product')

        role = Role.objects.get(user_id=request.user.id)

        product_categories = ProductCategory.objects.all()
        
        return render(request, 'a_product_detail_view.html', {'product': product, 'product_categories': product_categories, 'role': role.role})


class APIProductCreateView(View):
    def get(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        product_categories = ProductCategory.objects.all()

        role = Role.objects.get(user_id=request.user.id)

        return render(request, 'a_product_create_view.html', {'product_categories': product_categories, 'role': role.role})

    def post(self, request):
        unauthenticated_res = Util.redirect_if_unauthenticated(request)

        if unauthenticated_res is not None:
            return unauthenticated_res

        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        Product.objects.create(name=name, description=description, price=price, stock=stock, category_id=category, image=image)

        return redirect('a_product')