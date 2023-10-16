from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate


def index(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user= User.objects.get(email = email)
        except:
            messages.error(request, "the account doesn't exist")
        else:
            password = request.POST['password']
            user = authenticate(request, email=email, password =password)
            if user is None:
                messages.error(request, "email or password incorrect")
            else:
                login(request, user)
                account = Account.objects.get(client=user)
                try:
                    credit_card = CreditCard.objects.get(account=account)
                except:
                    return redirect("cashier:card_activation")
                else:
                    return redirect('cashier:menu')       

    context = {

    }
    return render(request, "cashier/index.html", context )


def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            account = Account.objects.create(client=user)
            try:
                credit_card = CreditCard.objects.get(account=account)
            except:
                return redirect("cashier:card_activation")
            else:
                return redirect('cashier:menu')       

        else:
            messages.error(request, "something went wrong during registration")
    form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'cashier/sign_up.html', context)



def card_activation(request):
    if request.method == 'POST':
        form = CardActivation(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            account = Account.objects.get(client=request.user)
            card.account = account
            card.save()
            return redirect('cashier:menu')       
    form = CardActivation()
    context = {
        'form': form
    }
    return render(request, 'cashier/card_activation.html', context)


def menu(request):
    context = {

    }
    return render(request, 'cashier/menu.html', context)


def logout_user(request):
    logout(request)
    return redirect('cashier:index')