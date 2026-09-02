from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'status',
    )
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = (
        'patient__name',
        'doctor__name',
        'patient__email',
        'doctor__email',
    )
    ordering = ('-appointment_date', '-appointment_time')
