from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'capacity', 'is_available', 'location')
    list_filter = ('is_available', 'location')
    search_fields = ('table_number', 'location')
    list_editable = ('is_available',)
    ordering = ('table_number',)

    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(request, "Selected tables have been marked as available.")
    make_available.short_description = "Mark selected tables as available"

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(request, "Selected tables have been marked as unavailable.")
    make_unavailable.short_description = "Mark selected tables as unavailable"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('table', 'reservation_time', 'number_of_guests', 'customer_name', 'customer_phone', 'status')
    list_filter = ('status', 'reservation_time', 'table')
    search_fields = ('customer_name', 'customer_phone', 'table__table_number')
    list_editable = ('status',)
    date_hierarchy = 'reservation_time'
    ordering = ('-reservation_time',)

    actions = ['confirm_reservations', 'cancel_reservations']

    def confirm_reservations(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, "Selected reservations have been confirmed.")
    confirm_reservations.short_description = "Confirm selected reservations"

    def cancel_reservations(self, request, queryset):
        queryset.update(status='canceled')
        self.message_user(request, "Selected reservations have been canceled.")
    cancel_reservations.short_description = "Cancel selected reservations"