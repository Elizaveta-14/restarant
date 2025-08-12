from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from reservation.models import Reservation


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('users:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Вы вошли в систему!")
            return redirect('users:profile')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})





def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect('reservation:home')


@login_required
def personal_cabinet(request):
    my_bookings = Reservation.objects.filter(user=request.user).order_by('-reservation_time')
    return render(request, 'users/profile.html', {'reservations': my_bookings})
