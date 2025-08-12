
from .forms import FeedbackForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Table, Reservation
from .forms import ReservationForm
from django.utils import timezone


def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваше сообщение! Мы скоро свяжемся с вами.')
            return redirect('reservation:home')
    else:
        form = FeedbackForm()

    return render(request, 'reservation/home.html', {'form': form})


def about(request):
    return render(request, 'reservation/about.html')



@login_required
def booking_view(request):
    available_tables = Table.objects.all()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                res = form.save(commit=False)
                res.user = request.user
                conflict = Reservation.objects.filter(
                    table=res.table,
                    reservation_time=res.reservation_time
                ).exists()

                if conflict:
                    messages.error(request, 'Это время уже занято.')
                else:
                    res.save()
                    return redirect('users:profile')
    else:
        form = ReservationForm()

    return render(request, 'reservation/booking.html', {
        'form': form,
        'available_tables': available_tables
    })


@login_required
def booking_confirm(request):
    return render(request, 'reservation/booking_confirm.html')


@login_required
def cancel_reservation(request, pk):
    res = get_object_or_404(Reservation, pk=pk, user=request.user)
    res.status = 'cancelled'
    res.save()
    messages.success(request, 'Бронирование отменено.')
    return redirect('users:profile')


