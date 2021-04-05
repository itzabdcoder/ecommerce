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

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.CASCADE)
    order_id = models.CharField(max_length = 120, default = "ABC" , unique = True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length = 120, choices = STATUS_CHOICES, default = "Started")
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places= 2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)

    def __str__(self):
        return str(self.order_id)

    def get_final_amount(self):
        instance = Order.objects.get(id=self.id)
        instance.tax_total = 0.08 * float(self.sub_total)
        instance.final_total = float(self.sub_total) + float(instance.tax_total)
        instance.save()
        return instance.final_total