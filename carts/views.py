from decimal import Decimal
from django.shortcuts import render, HttpResponseRedirect
from .models import Cart, CartItem
from django.urls import reverse
from products.models import Product, Variation
# Create your views here.
def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        context = {"cart": cart}
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total =  float(item.product.price) * item.quantity 
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        two_dec_digits = Decimal(10)  ** -2
        cart.total = Decimal(new_total).quantize(two_dec_digits)
        cart.save()
    else:
        message = "Your Cart is EMPTY"
        context = {"empty": True, "message": message}
    template = 'cart/view.html'
    return render(request, template, context)

def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse("cart"))
    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    # cartitem.cart = None
    # cartitem.save()
    return HttpResponseRedirect(reverse("cart"))


def add_to_cart(request, slug):
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist: 
        pass
    except:
        pass
    
    product_var = []
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product = product, category__iexact = key, title__iexact = val)
                product_var.append(v)
            except:
                pass

        cart_item = CartItem.objects.create(cart=cart,product=product)

        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()
        return HttpResponseRedirect(reverse("cart"))
    return HttpResponseRedirect(reverse("cart"))