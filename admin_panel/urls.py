from django.urls import path
from admin_panel.views import *


urlpatterns = [
    path('logs/', admin_view_logs, name='admin_view_logs'),
    path('backup/', backup_db, name='backup_db'),
    path('restore/', restore_db, name='restore_db'),
    path('users/', admin_user_list, name='admin_user_list'),
    path('users/<int:pk>/edit/', admin_user_edit, name='admin_user_edit'),
    path('users/<int:pk>/delete/', admin_user_delete, name='admin_user_delete'),
    path('users/<int:pk>/restore/', admin_user_restore, name='admin_user_restore'),
    path('users/create/', admin_user_create, name='admin_user_create'),
]