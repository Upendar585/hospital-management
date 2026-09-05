from appointments.models import Appointment
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction

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
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'doctor_login.html', {'error': 'Email and password are required'})

        # The Django admin can create a user with any username.  The doctor
        # login form, however, deliberately uses the doctor's email address.
        # Look up that user first, then authenticate with the stored username.
        # This also keeps accounts created before this change working.
        user_account = User.objects.filter(email__iexact=email).first()
        username = user_account.username if user_account else email
        user = authenticate(request, username=username, password=password)

        if user is not None:
            doctor = Doctor.objects.filter(user=user).first()

            # A user and doctor profile are often created separately in the
            # admin.  If their email addresses match, safely complete the
            # missing one-to-one link the first time the doctor logs in.
            if doctor is None and user.email:
                with transaction.atomic():
                    doctor = (
                        Doctor.objects.select_for_update()
                        .filter(user__isnull=True, email__iexact=user.email)
                        .first()
                    )
                    if doctor is not None:
                        doctor.user = user
                        doctor.save(update_fields=['user'])

            if doctor is not None:
                login(request, user)
                return redirect('doctor_dashboard')

            return render(
                request,
                'doctor_login.html',
                {
                    'error': (
                        'This account is not linked to a doctor profile. '
                        'Ask an administrator to create the doctor profile '
                        'and assign this user.'
                    )
                }
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
