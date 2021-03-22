"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,re_path
from django.conf import settings
from django.conf.urls.static import static

from products import views
from carts import views as cartviews
from orders import views as orderviews
from accounts import views as accountviews
from marketing import views as marketingviews
urlpatterns = [
    path('admin/', admin.site.urls),

    # urls of products app
    path('', views.home, name = 'home'),
    path('s/', views.search, name = 'search'),
    path('products/', views.products, name = 'products'),
    re_path(r'^products/(?P<slug>[\w-]+)/$' , views.single, name='single_product'),

    # urls of cart app
    re_path(r'^cart/(?P<id>\d+)/$' , cartviews.remove_from_cart, name='remove_from_cart'),
    re_path(r'^cart/(?P<slug>[\w-]+)/$' , cartviews.add_to_cart, name='add_to_cart'),
    re_path(r'^cart/$', cartviews.view, name = 'cart'),
    re_path(r'^checkout/$', orderviews.checkout, name = 'checkout'),

    # urls of order app
    re_path(r'^orders/$', orderviews.orders, name = 'user_order'),

    # urls of accounts app
    re_path(r'^accounts/logout/$', accountviews.logout_view, name = 'auth_logout'),
    re_path(r'^accounts/login/$', accountviews.login_view, name = 'auth_login'),
    re_path(r'^accounts/register/$', accountviews.registration_view, name = 'auth_register'),
    re_path(r'^accounts/activate/(?P<activation_key>\w+)$', accountviews.activation_view, name = 'activation_view'),

    # urls of marketing app
    re_path(r'^ajax/dismiss_marketing_message/$', marketingviews.dismiss_marketing_message, name = 'dismiss_marketing_message'),
    re_path(r'^ajax/email_signup/$', marketingviews.email_signup, name = 'ajax_email_signup'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)