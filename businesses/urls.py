from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerAboutUsView.as_view(), name='c_about'),
]