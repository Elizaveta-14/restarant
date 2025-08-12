from django.urls import path
from reservation import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'reservation'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/confirm/', views.booking_confirm, name='booking_confirm'),
    path('cancel/<int:pk>/', views.cancel_reservation, name='cancel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)