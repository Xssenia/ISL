from django.urls import path
from admin_panel.views import log_list

urlpatterns = [
    path('', log_list, name='log_list'),
]
