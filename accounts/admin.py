from django.contrib import admin

from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp
# Register your models here.

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)

class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['email','timestamp']
    class Meta:
        model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp)