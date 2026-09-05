from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Doctor


class DoctorLoginTests(TestCase):
    def test_doctor_can_log_in_with_email_when_username_is_different(self):
        user = User.objects.create_user(
            username='dr.ada',
            email='ada@example.com',
            password='secure-test-password',
        )
        doctor = Doctor.objects.create(
            name='Dr. Ada',
            specialization='Cardiology',
            phone='1234567890',
            email='ada@example.com',
            experience=5,
        )

        response = self.client.post(
            reverse('doctor_login'),
            {'email': 'ada@example.com', 'password': 'secure-test-password'},
        )

        self.assertRedirects(response, reverse('doctor_dashboard'))
        doctor.refresh_from_db()
        self.assertEqual(doctor.user, user)
