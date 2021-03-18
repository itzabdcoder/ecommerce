from django.conf import settings
from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class MarketingMessageQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)\
                    .filter(start_date__lt=timezone.now())\
                    .filter(end_date__lt=timezone.now())

class MarketingMessageManager(models.Manager):
    def get_queryset(self):
        return MarketingMessageQueryset(self.model ,using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().active().featured()

    def get_featured_item(self):
        print("hii")
        try:
            return self.get_queryset().active().featured()[0]
        except:
            return None

class MarketingMessage(models.Model):
    message = models.CharField(max_length=120)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    objects = MarketingMessageManager()

    def __str__(self):
        return str(self.message[:12])

    class Meta:
        ordering = ["-start_date","-end_date"]

def slider_upload(instance, filename):
    return "images/marketing/slider/%s" %(filename)

class Slider(models.Model):
    image = models.ImageField(upload_to=slider_upload)
    order = models.IntegerField(default=0)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    objects = MarketingMessageManager()

    def __str__(self):
        return str(self.image)

    def get_image_url(self):
        return "%s/%s" %(settings.MEDIA_URL, self.image)

    class Meta:
        ordering = ["order","-start_date","-end_date"]