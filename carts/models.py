from itertools import product
from django.db import models


class Cart(models.Model):
    pass

class CartItem(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
