from django.db import models
import django.utils.timezone
from datetime import datetime

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=150)
    page_id = models.CharField(max_length=150, default='')
    deadline = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    result_url = models.CharField(max_length=150, default='')

    def __str__(self):
        return self.name
