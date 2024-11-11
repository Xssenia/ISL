from django.shortcuts import render
from .models import Log

def log_list(request):
    logs = Log.objects.all()
    return render(request, 'logs/log_list.html', {'logs': logs})
