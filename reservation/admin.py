from django.contrib import admin
from .models import Table, Reservation, SiteContent

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats')
    search_fields = ('number',)
    ordering = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('table', 'reservation_time', 'customer_name', 'status')
    list_filter = ('status', 'reservation_time')
    search_fields = ('customer_name', 'customer_phone')
    ordering = ('reservation_time',)



@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'section', 'title')
    search_fields = ('page', 'section', 'title')