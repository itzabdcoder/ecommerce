from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    category = models.ManyToManyField('Category',blank=True)
    price = models.DecimalField(decimal_places = 2, max_digits = 100, default = 19.99)
    sale_price = models.DecimalField(decimal_places = 2, max_digits = 100, null = True, blank = True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    update_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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

class Category(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def product_defaults(sender, instance, created, *args, **kwargs):
    if instance.update_default:
        categories = instance.category.all()
        print(categories)
        for cat in categories:
            if cat.id == 1:
                small_size = Variation.objects.get_or_create(product=instance,category='size',title='Small')
                medium_size = Variation.objects.get_or_create(product=instance,category='size',title='Medium')
                large_size = Variation.objects.get_or_create(product=instance,category='size',title='Large')
        instance.update_default = False
        instance.save()

post_save.connect(product_defaults, sender=Product)