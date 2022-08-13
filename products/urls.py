from django.urls import path
from . import views

urlpatterns = [
    path('api/create', views.AdminProductCreateView.as_view(), name='a_product_create'),
    path('api/<product_id>', views.AdminProductDetailView.as_view(), name='a_product_detail'),
    path('api/', views.AdminProductView.as_view(), name='a_product',),
    path('detail/<product_id>/', views.CustomerProductDetailView.as_view(), name='c_product_detail'),
    path('detail/', views.CustomerProductDetailView.as_view(), name='c_product_detail'),
    path('<category_id>/', views.CustomerProductView.as_view(), name='c_product'),
    path('', views.CustomerProductView.as_view(), name='c_product'),
]