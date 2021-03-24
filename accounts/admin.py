from django.contrib import admin

from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress
# Register your models here.

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)

class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['email','timestamp']
    class Meta:
        model = EmailMarketingSignUp

admin.site.register(EmailMarketingSignUp)

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserAddress)