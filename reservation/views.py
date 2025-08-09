from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import Table, Reservation
from .forms import ReservationForm  # Предполагается, что вы создадите форму
from datetime import datetime, timedelta


def reservation_list(request):
    """Отображает список всех броней."""
    reservations = Reservation.objects.all().order_by('reservation_time')
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})


def create_reservation(request):
    """Создает новую бронь."""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Проверка доступности стола
            table = form.cleaned_data['table']
            reservation_time = form.cleaned_data['reservation_time']
            number_of_guests = form.cleaned_data['number_of_guests']

            # Проверка, что стол доступен в указанное время
            existing_reservation = Reservation.objects.filter(
                table=table,
                reservation_time=reservation_time,
                status__in=['pending', 'confirmed']
            ).exists()

            if existing_reservation:
                messages.error(request, "This table is already reserved at the specified time.")
            elif number_of_guests > table.capacity:
                messages.error(request, "Number of guests exceeds table capacity.")
            else:
                form.save()
                messages.success(request, "Reservation created successfully!")
                return redirect('reservation_list')
    else:
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})


def cancel_reservation(request, reservation_id):
    """Отменяет существующую бронь."""
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, "Reservation cancelled successfully!")
        return redirect('reservation_list')

    return render(request, 'reservations/cancel_reservation.html', {'reservation': reservation})


def available_tables(request):
    """Отображает список доступных столов для бронирования в указанное время."""
    if request.method == 'POST':
        reservation_time = request.POST.get('reservation_time')
        try:
            reservation_time = datetime.strptime(reservation_time, '%Y-%m-%dT%H:%M')
            reservation_time = timezone.make_aware(reservation_time)

            # Найти столы, которые не забронированы в указанное время
            reserved_tables = Reservation.objects.filter(
                reservation_time=reservation_time,
                status__in=['pending', 'confirmed']
            ).values_list('table_id', flat=True)

            available_tables = Table.objects.filter(is_available=True).exclude(id__in=reserved_tables)
            return render(request, 'reservations/available_tables.html', {
                'tables': available_tables,
                'reservation_time': reservation_time
            })
        except ValueError:
            messages.error(request, "Invalid date or time format.")

    return render(request, 'reservations/available_tables.html')