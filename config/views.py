from django.contrib.auth import authenticate, login
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            return render(request, 'admin_login.html', {'error': 'Email and password are required'})

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('/admin/')

            return render(
                request,
                'admin_login.html',
                {'error': 'This account does not have admin access.'}
            )

        return render(
            request,
            'admin_login.html',
            {'error': 'Invalid email or password'}
        )

    return render(request, 'admin_login.html')


def health(request):
    """Report application and database availability to the hosting platform."""
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return JsonResponse({'status': 'ok'})
