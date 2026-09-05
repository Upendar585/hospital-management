from django.test import TestCase
from django.urls import reverse

from doctors.models import Doctor


class BookingEntryTests(TestCase):
    def test_anonymous_booking_shows_role_login_choices(self):
        doctor = Doctor.objects.create(
            name='Dr. Taylor',
            specialization='General Medicine',
            phone='1234567890',
            email='taylor@example.com',
            experience=8,
        )

        response = self.client.get(reverse('book_appointment', args=[doctor.id]))

        self.assertRedirects(
            response,
            f'/?next=%2Fappointments%2Fbook%2F{doctor.id}%2F#choose-role',
            fetch_redirect_response=False,
        )
