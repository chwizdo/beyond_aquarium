from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerCartView.as_view(), name='c_cart'),
    path('checkout/', view=views.CustomerCheckoutView.as_view(), name='c_checkout'),
]