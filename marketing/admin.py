from django.contrib import admin
from .models import MarketingMessage
# Register your models here.
class MarketingMessageAdmin(admin.ModelAdmin):
    class Meta:
        model = MarketingMessage
    
admin.site.register(MarketingMessage, MarketingMessageAdmin)