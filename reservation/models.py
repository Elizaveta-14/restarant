from django.db import models
from django.conf import settings



class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Table(models.Model):
    number = models.IntegerField(verbose_name="Номер стола")
    seats = models.IntegerField(verbose_name="Количество мест")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Стол {self.number} ({self.seats} мест)"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Забронирован'),
        ('cancelled', 'Отменён'),
        ('completed', 'Завершён'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Стол")
    reservation_time = models.DateTimeField(verbose_name="Время бронирования")
    number_of_guests = models.PositiveIntegerField(verbose_name="Количество гостей")
    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Бронь стола {self.table.number} — {self.customer_name} ({self.reservation_time.strftime('%d.%m.%Y %H:%M')})"


class SiteContent(models.Model):
    page = models.CharField(max_length=100, verbose_name="Страница")
    section = models.CharField(max_length=100, verbose_name="Раздел")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Текст")
    image = models.ImageField(upload_to='site_images/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Контент сайта"
        verbose_name_plural = "Контент сайта"

    def __str__(self):
        return f"{self.page} — {self.section}"





