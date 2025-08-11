from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('cancel/<int:pk>/', views.cancel_reservation, name='cancel_reservation'),
]
