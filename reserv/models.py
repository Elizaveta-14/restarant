from django.db import models

# Create your models here.
from django.db import models
from django.db.models import CharField
from users.models import User
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = [
            "name",
        ]


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(verbose_name="описание", null=True, blank=True)
    image = models.ImageField(verbose_name="изображение", null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.BigIntegerField(verbose_name="цена")
    created_at = models.DateField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateField(
        auto_now=True, verbose_name="дата последнего изменения"
    )
    views_counter = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False, verbose_name="Доступность в каталоге")
    owner = models.ForeignKey(User, verbose_name='имя владельца', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = [
            "name",
        ]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("remove_any_product", "Remove any product"),
        ]
