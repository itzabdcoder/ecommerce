from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
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
        return HttpResponseRedirect(reverse("cart"))
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
            # print(customer)
        except:
            customer = None
            pass
        if customer is not None:
            token = request.POST['stripeToken']
            card = stripe.Customer.create_source(
                customer.id,
                source="tok_visa",
                # "address" => ["city" => $city, "country" => $country, "line1" => $address, "line2" => "", "postal_code" => $zipCode, "state" => $state]
            )
            charge = stripe.Charge.create(
                amount=int(new_order.final_total * 100),
                currency="inr",
                source="tok_visa",
                description="Charge for %s" %(request.user.username),
            )
        if charge['captured']:
            print('charged')
        print(card)
        print(charge)
    
    context = {
        "order": new_order,
        "address_form":address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses,
        "stripe_pub": stripe_pub,
        }
    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))
    template = "orders/checkout.html"
    return render(request, template, context)