from django.db import models

# Create your models here.
class hmData(models.Model):
    username = models.CharField(max_length=256)
    content = models.TextField()
    time = models.TextField()
    def __str__(self):
        return self.username