from django.urls import path
from . import views

urlpatterns = [
    path('api/<order_id>/', views.APIOrderDetailView.as_view(), name='a_order_detail'),
    path('api/', views.APIOrderView.as_view(), name='a_order'),
    path('<order_id>/', views.CustomerOrderDetailView.as_view(), name='c_order_detail'),
    path('', views.CustomerOrderView.as_view(), name='c_order'),
]