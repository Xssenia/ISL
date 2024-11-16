from django.shortcuts import render
from .models import Log

def log_list(request):
    logs = Log.objects.all()
    return render(request, 'logs/log_list.html', {'admin_panel': logs})

def log_action(user, action_type, entity, entity_id, details=None):
    Log.objects.create(
        user=user,
        type=action_type,
        entity=entity,
        entityID=entity_id,
        action_details=details
    )