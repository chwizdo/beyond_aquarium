from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)

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
