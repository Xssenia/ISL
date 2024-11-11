from django.urls import path
from .views import create_backup, restore_backup

urlpatterns = [
    path('create/', create_backup, name='create_backup'),
    path('restore/', restore_backup, name='restore_backup'),
]
