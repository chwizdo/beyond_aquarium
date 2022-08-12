from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomerLoginView.as_view(), name='c_login'),
    path('signup/', views.CustomerSignUpView.as_view(), name='c_signup'),
    path('profile/', views.CustomerProfileDetailView.as_view(), name='c_profile_detail'),
    path('logout/', views.CustomerLogoutView.as_view(), name='c_logout'),
]