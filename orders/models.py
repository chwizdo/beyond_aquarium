from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    postcode = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.street


class OrderItem(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=256)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
