from django.urls import reverse
from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(decimal_places = 2, max_digits = 100, default = 19.99)
    sale_price = models.DecimalField(decimal_places = 2, max_digits = 100, null = True, blank = True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "This is a Product"

    def get_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse("single_product", kwargs = {"slug" : self.slug})

    class Meta:
        unique_together = ('title','slug')

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.title

class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    
    def colors(self):
        return self.all().filter(category='color')
    
    def sizes(self):
        return self.all().filter(category='size')
        

VAR_CATEGORIES = (
    ('size','size'),
    ('color','color'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    category = models.CharField(max_length = 100, choices = VAR_CATEGORIES, default = 'size')
    title = models.CharField(max_length = 100)
    image = models.ForeignKey(ProductImage,null = True, blank = True, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places = 2, max_digits = 100, null = True, blank = True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(default=timezone.now)

    objects = VariationManager()

    def __str__(self):
        return self.title