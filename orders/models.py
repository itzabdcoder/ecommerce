from accounts.models import UserAddress
from decimal import Decimal
from django.db import models
from django.conf import settings

# Create your models here.
from carts.models import Cart
from django.utils import timezone


STATUS_CHOICES=(
    ("Started","Started"),
    ("Abandoned","Abandoned"),
    ("Finished","Finished"),
)

try:
    tax_rate = settings.DEFAULT_TAX_RATE
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    order_id = models.CharField(max_length = 120, default = "ABC" , unique = True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length = 120, choices = STATUS_CHOICES, default = "Started")
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', on_delete=models.CASCADE, null=True,blank=True)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address', on_delete=models.CASCADE, null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places= 2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)

    def __str__(self):
        return str(self.order_id)

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        two_dec_digits = Decimal(10) ** -2
        tax_rate_dec = Decimal("%s" %(tax_rate))
        sub_total_dec = Decimal(self.sub_total)
        tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_dec_digits)
        instance.tax_total = tax_total_dec
        instance.final_total = sub_total_dec + tax_total_dec
        instance.save()
        return instance.final_total