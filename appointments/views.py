from datetime import datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .models import Appointment
from doctors.models import Doctor
from users.models import Patient


@login_required
def book_appointment(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id, available=True)
    patient = Patient.objects.filter(user=request.user).first()

    if patient is None:
        messages.error(request, 'Only patient accounts can book appointments.')
        return redirect('doctor_list')

    if request.method == 'POST':

        appointment_date = request.POST.get('appointment_date', '')
        appointment_time = request.POST.get('appointment_time', '')
        reason = request.POST.get('reason', '').strip()

        try:
            scheduled_at = datetime.strptime(
                f'{appointment_date} {appointment_time}', '%Y-%m-%d %H:%M'
            )
        except ValueError:
            messages.error(request, 'Please select a valid appointment date and time.')
            return render(request, 'book_appointment.html', {'doctor': doctor})

        if scheduled_at < datetime.now():
            messages.error(request, 'Appointments must be scheduled for a future date and time.')
            return render(request, 'book_appointment.html', {'doctor': doctor})

        if not reason:
            messages.error(request, 'Please describe the reason for your visit.')
            return render(request, 'book_appointment.html', {'doctor': doctor})

        if Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date,
                                      appointment_time=appointment_time,
                                      status__in=['Pending', 'Confirmed']).exists():
            messages.error(request, 'That time is no longer available. Please choose another time.')
            return render(request, 'book_appointment.html', {'doctor': doctor})

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason
        )

        messages.success(request, 'Your appointment request has been sent to the doctor.')
        return redirect('patient_dashboard')

    return render(
        request,
        'book_appointment.html',
        {'doctor': doctor}
    )
