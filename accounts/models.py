from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from localflavor.in_.in_states import STATE_CHOICES
# Create your models here.

class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", null=True, blank=True, related_name="user_default_shipping_address", on_delete=models.CASCADE)
    billing = models.ForeignKey("UserAddress", null=True, blank=True, related_name="user_default_billing_address", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)

class UserAddressManager(models.Manager):
    def get_billing_addresses(self,user):
        return super(UserAddressManager, self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, choices=STATE_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    zipcode = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=100)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    objects = UserAddressManager()

    class Meta:
        ordering = ['-updated','-timestamp']

    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.address, self.city, self.state, self.country, self.zipcode)
        
    def __str__(self):
        return self.get_address()

class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length = 120, null = True, blank = True)

    def __str__(self):
        return str(self.stripe_id)

class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default = False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        activation_url = "http://localhost:8000%s" %(reverse("activation_view",args=[self.activation_key]))
        context = {
            "activation_key" : self.activation_key,
            "activation_url" : activation_url,
            "user" : self.user.username
        }
        subject = "Activate your Email"
        message = render_to_string('accounts/activation_message.txt',context)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email= None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)

class EmailMarketingSignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)