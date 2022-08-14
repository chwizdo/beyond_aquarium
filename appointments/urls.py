from django.urls import path
from . import views

urlpatterns = [
    path('feedback/api/<feedback_id>', views.AdminFeedbackDetailView.as_view(), name='a_feedback_detail'),
    path('feedback/api/', views.AdminFeedbackView.as_view(), name='a_feedback'),
    path('api/<appointment_id>/', views.AdminAppointmentDetailView.as_view(), name='a_appointment_detail'),
    path('api/', views.AdminAppointmentView.as_view(), name='a_appointment'),
    path('', views.CustomerContactUsView.as_view(), name='c_contact'),
]