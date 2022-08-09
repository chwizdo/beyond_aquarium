from unicodedata import category
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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
    if not request.user.is_authenticated:
      return redirect('c_login')

    if product_id is None:
        return redirect('c_product')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('c_product')

    return render(request, 'c_product_detail_view.html', {'product': product})