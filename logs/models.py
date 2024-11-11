from django.db import models
from users.models import User

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    entity = models.CharField(max_length=255)
    entityID = models.IntegerField()
    action_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.type} - {self.entity}"

# logs/models.py
def log_action(user, action_type, entity, entity_id, details=None):
    from .models import Log
    Log.objects.create(
        user=user,
        type=action_type,
        entity=entity,
        entityID=entity_id,
        action_details=details
    )
