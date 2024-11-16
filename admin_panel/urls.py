from django.urls import path
from admin_panel.views import admin_view_logs

urlpatterns = [
    path('logs/', admin_view_logs, name='admin_view_logs'),

]
