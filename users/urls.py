from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_patient, name='register'),
    path('login/', views.patient_login, name='login'),
    path('logout/', views.patient_logout, name='logout'),
    path(
        'appointment/<int:appointment_id>/cancel/',
        views.cancel_patient_appointment,
        name='cancel_patient_appointment',
    ),
]
