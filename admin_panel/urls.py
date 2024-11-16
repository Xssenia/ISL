from django.urls import path
from admin_panel.views import admin_view_logs, backup_db, restore_db
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logs/', admin_view_logs, name='admin_view_logs'),
    path('backup/', backup_db, name='backup_db'),
    path('restore/', restore_db, name='restore_db'),
]
