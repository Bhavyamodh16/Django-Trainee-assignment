from django.db import models

class Log(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This bypasses the registry check and maps it directly to myapp
        app_label = 'myapp'

    def __str__(self):
        return self.message
