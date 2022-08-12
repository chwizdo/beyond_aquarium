from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    USER_ROLE = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=USER_ROLE, max_length=256)
