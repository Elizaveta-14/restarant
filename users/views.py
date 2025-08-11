from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from reservation.models import Reservation
from reservation.forms import ReservationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('users:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_time')
    return render(request, 'users/profile.html', {'reservations': reservations})


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование обновлено.')
            return redirect('users:profile')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'users/edit_reservation.html', {'form': form})


@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    reservation.status = 'cancelled'
    reservation.save()
    messages.success(request, 'Бронирование отменено.')
    return redirect('users:profile')
