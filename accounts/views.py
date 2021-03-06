import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from .models import EmailConfirmed
from .forms import LoginForm, RegistrationForm
# Create your views here.
def logout_view(request):
    logout(request)
    messages.warning(request, "Successfully Logged Out.<strong> <a href='%s' class='alert-link'>Login</a></strong> again?" %(reverse('auth_login')),extra_tags='safe')
    return HttpResponseRedirect(reverse('auth_login'))

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,password=password)
        login(request,user)
        messages.success(request, "<strong>Logged In</strong>",extra_tags='safe')
        return HttpResponseRedirect('/')
    
    context = {"form":form, "logging": True}
    return render(request, "form.html", context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit = False)
        new_user.first_name = 'Admin'
        new_user.save()
        messages.success(request, "Successfully Registered. Confirm your mail first.")
        return HttpResponseRedirect("/")

    context = {"form":form}
    return render(request, "form.html", context)

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful" 
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed"
        else:
            page_message = ""
        
        context = {
            "page_message" : page_message
        }

        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404