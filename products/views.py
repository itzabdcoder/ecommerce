from django.shortcuts import render, Http404
from .models import Product, ProductImage
from marketing.models import MarketingMessage, Slider
# Create your views here.
def home(request):
    sliders = Slider.objects.all()
    product = Product.objects.all()
    template = 'products/home.html'
    context = {
        "products": product,
        "sliders": sliders,
    }
    return render(request, template, context)

def products(request):
    product = Product.objects.all()
    template = 'products/all.html'
    context = {"products": product}
    return render(request, template, context)

def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = none
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {"query": q,"products": products}
        template = 'products/results.html'
    else:
        template = 'products/home.html'
        context = {}
    return render(request, template, context)

def single(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        # images = ProductImage.objects.filter(product=product)
        images = product.productimage_set.all()
        template = 'products/single.html'
        context = {"product": product, "images": images}
        return render(request, template, context)
    except:
        raise Http404
