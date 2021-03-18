from django.contrib import admin
from .models import MarketingMessage, Slider
# Register your models here.
class MarketingMessageAdmin(admin.ModelAdmin):
    list_display = ["__str__","start_date","end_date","active","featured"]
    class Meta:
        model = MarketingMessage
    
admin.site.register(MarketingMessage, MarketingMessageAdmin)

class SliderAdmin(admin.ModelAdmin):
    list_display = ["__str__","start_date","end_date","url_link"]
    list_editable = ["start_date","end_date","url_link"]
    class Meta:
        model = Slider

admin.site.register(Slider, SliderAdmin)