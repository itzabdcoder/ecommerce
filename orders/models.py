from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from carts.models import Cart
from django.utils import timezone

User = get_user_model()

STATUS_CHOICES=(
    ("Started","Started"),
    ("Abandoned","Abandoned"),
    ("Finished","Finished"),
)

class Order(models.Model):
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    order_id = models.CharField(max_length = 120, default = "ABC" , unique = True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length = 120, choices = STATUS_CHOICES, default = "Started")
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places= 2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)

    def __str__(self):
        return str(self.id)