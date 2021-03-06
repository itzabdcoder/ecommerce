from django.db import models
from django.utils import timezone

# Create your models here.
class MarketingMessage(models.Model):
    message = models.CharField(max_length=120)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.message[:12])
