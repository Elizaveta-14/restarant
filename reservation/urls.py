from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .apps import ReservationConfig

app_name = ReservationConfig.name

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("contacts/", views.ContactsListView.as_view(), name="contacts"),
    path("table_list/", views.TableListView.as_view(), name="table_list"),
    path("tables/<int:pk>/", cache_page(60)(views.TableDetailView.as_view()), name="table_detail"),
    path("tables/create/", views.TableCreateView.as_view(), name="table_create"),
    path("tables/<int:pk>/delete/", views.TableDeleteView.as_view(), name="table_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)