from django.contrib import admin

from .models import UserStripe, EmailConfirmed
# Register your models here.

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)