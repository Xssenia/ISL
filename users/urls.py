# users/urls.py
from django.urls import path

from . import views
from .views import register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('my_reservations/', views.user_reservations_and_loans, name='user_reservations_and_loans'),
]
