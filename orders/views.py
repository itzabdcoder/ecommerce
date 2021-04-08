from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator
import time
import stripe
# Create your views here.

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    print(str(e))
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

def orders(request):
    context = {}
    template = "orders/user.html"
    return render(request, template, context)

@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("cart"))
    try:
        new_order = Order.objects.get(cart = cart)
    except Order.DoesNotExist:
        new_order = Order() 
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        new_order = None
        return HttpResponseRedirect(reverse("cart"))
    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()
    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None
    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user)

    if request.method == 'POST':
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None
            pass
        if customer is not None:
            billing_add = request.POST['billing_address']
            shipping_add = request.POST['shipping_address']
            token = request.POST['stripeToken']
            try:
                shipping_address_instance = UserAddress.objects.get(id=shipping_add)
            except:
                shipping_address_instance = None
            try:
                billing_address_instance = UserAddress.objects.get(id=billing_add)
            except:
                billing_address_instance = None
            card = stripe.Customer.create_source(
                customer.id,
                source="tok_visa",
            )
            card.address_line1 = billing_address_instance.address or None
            card.address_line2 = billing_address_instance.address2 or None
            card.address_city = billing_address_instance.city or None
            card.address_zip = billing_address_instance.zipcode or None
            card.address_state = billing_address_instance.state or None
            card.address_country = billing_address_instance.country or None
            print(card.address_country)
            print(card.address_line1)
            card.save()
            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="inr",
                source="tok_visa",
                description="Charge for %s" %(request.user.username),
            )
        if charge['captured']:
            new_order.status = "Finished"
            new_order.shipping_address = shipping_address_instance
            new_order.billing_address = billing_address_instance
            new_order.save()
            del request.session['cart_id']
            del request.session['items_total']
            messages.success(request, "Your Cart Products has been purchased refer <a href='https://dashboard.stripe.com/test/payments'> https://dashboard.stripe.com/test/payments </a>",extra_tags='safe')
            return HttpResponseRedirect(reverse("user_order"))
    
    context = {
        "order": new_order,
        "address_form":address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses,
        "stripe_pub": stripe_pub,
        }
    template = "orders/checkout.html"
    return render(request, template, context)