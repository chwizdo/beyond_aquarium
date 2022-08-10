from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerOrderView.as_view(), name='c_order'),
    path('<order_id>/', views.CustomerOrderDetailView.as_view(), name='c_order_detail'),
]