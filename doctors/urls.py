from django.urls import path

from .views import (
    doctor_list,
    doctor_login,
    doctor_dashboard,
    doctor_logout,
    confirm_appointment,
    cancel_appointment,
    complete_appointment
)

urlpatterns = [
    path('', doctor_list, name='doctor_list'),

    path('login/', doctor_login, name='doctor_login'),

    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),

    path(
        'appointment/<int:appointment_id>/confirm/',
        confirm_appointment,
        name='confirm_appointment'
    ),

    path(
        'appointment/<int:appointment_id>/cancel/',
        cancel_appointment,
        name='cancel_appointment'
    ),

    path(
        'appointment/<int:appointment_id>/complete/',
        complete_appointment,
        name='complete_appointment'
    ),

    path('logout/', doctor_logout, name='doctor_logout'),
]