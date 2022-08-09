from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

