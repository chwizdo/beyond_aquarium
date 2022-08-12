from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomerLoginView.as_view(), name='c_login'),
    path('signup/', views.CustomerSignUpView.as_view(), name='c_signup'),
    path('profile/', views.CustomerProfileDetailView.as_view(), name='c_profile_detail'),
    path('logout/', views.CustomerLogoutView.as_view(), name='c_logout'),
    path('admin/create', views.AdminUserCreationView.as_view(), name='a_user_create'),
    path('admin/<user_id>', views.AdminUserDetailView.as_view(), name='a_user_detail'),
    path('admin/', views.AdminUserView.as_view(), name='a_user'),
]