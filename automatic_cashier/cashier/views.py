from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        return redirect('cashier:menu')
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


@login_required(login_url='cashier:index')
def logout_user(request):
    logout(request)
    return redirect('cashier:index')


@login_required(login_url='cashier:index')
def check_balance(request):
    user = request.user
    account = Account.objects.get(client=user)
    context = {
        'account': account
    }
    return render(request, 'cashier/check_balance.html', context)

@login_required(login_url='cashier:index')
def card_validation(request, trans):
    user = request.user
    account = Account.objects.get(client=user)
    card = CreditCard.objects.get(account = account)
    tries = 0
    # task for new session: fix the try loop problem
    if request.method == 'POST':
        if card.password == request.POST['card-password']:
            if trans == 1:
                return redirect('cashier:check_balance')
        else:
            tries += 1
            if tries == card.id_limit:
                card.activation=False
                card.save()
                messages.error(request, f'wrong password, your credit card has been blocked')

                return redirect('cashier:menu')
            messages.error(request, f'wrong password, you have {3-tries} left')
            context = {
                'tries': tries
            }
            
            return render(request, 'cashier/card_validation.html', context)
    context = {
        'tries': tries
    }
    return render(request, 'cashier/card_validation.html', context)