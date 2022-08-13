from django.urls import path
from . import views

urlpatterns = [
    path('feedback/api/', views.AdminFeedbackView.as_view(), name='a_feedback'),
    path('api/', views.AdminAppointmentView.as_view(), name='a_appointment'),
    path('', views.CustomerContactUsView.as_view(), name='c_contact'),
]