from django.db import models
from products.models import Product, Variation
from django.utils import timezone
# Create your models here.
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete = models.CASCADE, blank = True , null = True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank = True)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places= 2)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title


class Cart(models.Model):
    total = models.DecimalField(decimal_places = 2, max_digits = 100, default = 0.00)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id: %s" %(self.id)