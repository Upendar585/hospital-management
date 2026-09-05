from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Keep the staff account visibly connected to its doctor profile."""

    list_display = ('name', 'specialization', 'email', 'user', 'available')
    list_filter = ('available', 'specialization')
    search_fields = ('name', 'email', 'user__username', 'user__email')
    autocomplete_fields = ('user',)
    fieldsets = (
        (
            'Login account',
            {
                'fields': ('user',),
                'description': (
                    'Select the Django user account used by this doctor. '
                    'Use the same email address on the user and doctor records.'
                ),
            },
        ),
        (
            'Doctor details',
            {'fields': ('name', 'specialization', 'phone', 'email', 'experience', 'available')},
        ),
    )
