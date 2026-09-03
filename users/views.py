from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


def register_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        gender = request.POST.get('gender', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip().lower()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '')

        if not all([name, age, gender, phone, email, address, password]):
            messages.error(request, 'Please complete every field.')
            return render(request, 'register.html')

        if User.objects.filter(username=email).exists() or Patient.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists. Please log in instead.')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            Patient.objects.create(user=user, name=name, age=age, gender=gender,
                                   phone=phone, email=email, address=address)
        except (IntegrityError, ValueError):
            messages.error(request, 'We could not create your account. Please check your details and try again.')
            return render(request, 'register.html')

        login(request, user)
        messages.success(request, 'Registration successful. You can now choose a doctor and book an appointment.')
        return redirect('patient_dashboard')

    return render(request, 'register.html')


def patient_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Email and password are required'})

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            if not Patient.objects.filter(user=user).exists():
                return render(request, 'login.html', {'error': 'Please use the doctor login for this account.'})
            login(request, user)
            return redirect('/dashboard/')

        return render(
            request,
            'login.html',
            {'error': 'Invalid email or password'}
        )

    return render(request, 'login.html')


@login_required(login_url='login')
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)

    appointments = patient.appointments.select_related('doctor').order_by(
        'appointment_date', 'appointment_time'
    )
    doctors = Doctor.objects.filter(available=True).order_by('name')

    return render(
        request,
        'dashboard.html',
        {
            'patient': patient,
            'appointments': appointments,
            'doctors': doctors,
        }
    )


def patient_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='login')
def cancel_patient_appointment(request, appointment_id):
    patient = get_object_or_404(Patient, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    if request.method == 'POST' and appointment.status in ('Pending', 'Confirmed'):
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, 'Your appointment has been cancelled.')
    else:
        messages.error(request, 'This appointment can no longer be cancelled.')

    return redirect('patient_dashboard')
