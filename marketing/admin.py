from django.contrib import admin
from .models import MarketingMessage
# Register your models here.
class MarketingMessageAdmin(admin.ModelAdmin):
    list_display = ["__str__","start_date","end_date","active","featured"]
    class Meta:
        model = MarketingMessage
    
admin.site.register(MarketingMessage, MarketingMessageAdmin)