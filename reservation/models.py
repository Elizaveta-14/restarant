from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Table(models.Model):
    table_number = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    reservation_time = models.DateTimeField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Reservation for {self.customer_name} at {self.reservation_time}"

    def save(self, *args, **kwargs):
        if self.reservation_time < timezone.now():
            raise ValueError("Reservation time must be in the future.")
        if self.number_of_guests > self.table.capacity:
            raise ValueError("Number of guests exceeds table capacity.")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('table', 'reservation_time')