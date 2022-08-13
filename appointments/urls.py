from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerContactUsView.as_view(), name='c_contact'),
]