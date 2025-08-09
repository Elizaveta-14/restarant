from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.decorators.cache import cache_page
from catalog.views import ProductListView, ProductDetailView, HomeListView, ContactsListView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = ([
                   path("", HomeListView.as_view(), name="home"),
                   path("contacts/", ContactsListView.as_view(), name="contacts"),
                   path('products_list/', ProductListView.as_view(), name='table_list'),
                   path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='table_detail'),
                   path('products/create/', ProductCreateView.as_view(), name='table_create'),
                   path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='table_delete')
               ]

               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))