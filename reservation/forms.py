from django import forms
from django.utils import timezone
from .models import Table, Reservation
from datetime import datetime, timedelta


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'reservation_time', 'number_of_guests', 'customer_name', 'customer_phone']
        widgets = {
            'reservation_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор только доступными столами
        self.fields['table'].queryset = Table.objects.filter(is_available=True)

    def clean_reservation_time(self):
        """Проверяет, что время бронирования находится в допустимом диапазоне."""
        reservation_time = self.cleaned_data.get('reservation_time')
        now = timezone.now()

        # Время бронирования не может быть в прошлом
        if reservation_time < now:
            raise forms.ValidationError("Reservation time cannot be in the past.")

        # Проверяем, что бронирование делается не позже, чем за 7 дней
        max_future = now + timedelta(days=7)
        if reservation_time > max_future:
            raise forms.ValidationError("Reservation cannot be made more than 7 days in advance.")

        # Проверяем, что бронирование делается в рабочее время (например, с 10:00 до 22:00)
        hour = reservation_time.hour
        if hour < 10 or hour >= 22:
            raise forms.ValidationError("Reservations are only allowed between 10:00 and 22:00.")

        return reservation_time

    def clean_number_of_guests(self):
        """Проверяет, что количество гостей соответствует вместимости стола."""
        number_of_guests = self.cleaned_data.get('number_of_guests')
        table = self.cleaned_data.get('table')

        if table and number_of_guests > table.capacity:
            raise forms.ValidationError(f"Number of guests exceeds table capacity ({table.capacity}).")

        if number_of_guests <= 0:
            raise forms.ValidationError("Number of guests must be greater than 0.")

        return number_of_guests

    def clean(self):
        """Проверяет, что стол не забронирован в указанное время."""
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        reservation_time = cleaned_data.get('reservation_time')

        if table and reservation_time:
            # Проверяем, нет ли активных бронирований для этого стола в указанное время
            existing_reservation = Reservation.objects.filter(
                table=table,
                reservation_time=reservation_time,
                status__in=['pending', 'confirmed']
            ).exists()

            if existing_reservation:
                raise forms.ValidationError("This table is already reserved at the specified time.")

        return cleaned_data