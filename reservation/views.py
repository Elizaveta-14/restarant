from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Table
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

class HomeListView(ListView):
    template_name = 'reservations/home.html'
    context_object_name = 'tables'
    model = Table

    def get_queryset(self):
        return Table.objects.filter(is_available=True)


class ContactsListView(ListView):
    template_name = 'reservations/contacts.html'
    model = Table  # Можно заменить на другую модель, если contacts не связан с Table
    context_object_name = 'contacts'

    def get_queryset(self):
        return Table.objects.all()  # Или другая логика для контактов


class TableListView(ListView):
    template_name = 'reservations/table_list.html'
    model = Table
    context_object_name = 'tables'

    def get_queryset(self):
        return Table.objects.all()


class TableDetailView(DetailView):
    template_name = 'reservations/table_detail.html'
    model = Table
    context_object_name = 'table'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = self.object.reservation_set.all()  # Связанные бронирования
        return context


class TableCreateView(LoginRequiredMixin, CreateView):
    template_name = 'reservations/table_form.html'
    model = Table
    fields = ['table_number', 'capacity', 'is_available', 'location']
    success_url = reverse_lazy('reservations:table_list')


class TableDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'reservations/table_confirm_delete.html'
    model = Table
    success_url = reverse_lazy('reservations:table_list')