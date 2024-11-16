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