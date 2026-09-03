from django.contrib import admin
from django.urls import path, include

from .views import health, home, admin_login
from users.views import patient_dashboard


urlpatterns = [
    path('admin/login/', admin_login, name='admin_login'),

    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('health/', health, name='health'),

    path('doctors/', include('doctors.urls')),

    path('appointments/', include('appointments.urls')),

    path('', include('users.urls')),

    path('dashboard/', patient_dashboard, name='patient_dashboard'),
]