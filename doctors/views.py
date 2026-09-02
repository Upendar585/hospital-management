from appointments.models import Appointment
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Doctor


def doctor_required(view_func):
    """Allow doctor-only pages to be used only by authenticated doctors."""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not Doctor.objects.filter(user=request.user).exists():
            return HttpResponseForbidden('Access denied. This page is for doctors only.')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def doctor_list(request):
    doctors = Doctor.objects.all()

    return render(request, 'doctors.html', {
        'doctors': doctors
    })


def doctor_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            try:
                doctor = Doctor.objects.get(user=user)
                login(request, user)
                return redirect('doctor_dashboard')
            except Doctor.DoesNotExist:
                return render(
                    request,
                    'doctor_login.html',
                    {'error': 'This account is not registered as a doctor.'}
                )

        return render(
            request,
            'doctor_login.html',
            {'error': 'Invalid email or password'}
        )

    return render(request, 'doctor_login.html')


@login_required(login_url='doctor_login')
@doctor_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointments = doctor.appointments.select_related('patient').order_by(
        'appointment_date',
        'appointment_time'
    )

    return render(
        request,
        'doctor_dashboard.html',
        {
            'doctor': doctor,
            'appointments': appointments
        }
    )


def doctor_logout(request):
    logout(request)
    return redirect('home')
@login_required(login_url='doctor_login')
@doctor_required
def confirm_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointment = get_object_or_404(Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if request.method != 'POST' or appointment.status != 'Pending':
        return redirect('doctor_dashboard')

    appointment.status = 'Confirmed'
    appointment.save()
    messages.success(request, 'Appointment confirmed.')

    return redirect('doctor_dashboard')


@login_required(login_url='doctor_login')
@doctor_required
def cancel_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointment = get_object_or_404(Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if request.method != 'POST' or appointment.status not in ('Pending', 'Confirmed'):
        return redirect('doctor_dashboard')

    appointment.status = 'Rejected'
    appointment.save()
    messages.success(request, 'Appointment rejected.')

    return redirect('doctor_dashboard')


@login_required(login_url='doctor_login')
@doctor_required
def complete_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointment = get_object_or_404(Appointment,
        id=appointment_id,
        doctor=doctor
    )

    if request.method != 'POST' or appointment.status != 'Confirmed':
        return redirect('doctor_dashboard')

    appointment.status = 'Completed'
    appointment.save()
    messages.success(request, 'Appointment marked as completed.')

    return redirect('doctor_dashboard')
