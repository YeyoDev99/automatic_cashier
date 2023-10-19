from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
def check_balance(request, boolean):
    bool = bool(boolean)
    if not bool:
        return redirect('cashier:card_validation')
    else:
        pass


@login_required(login_url='cashier:index')
def card_validation(request):
    user = request.user
    account = Account.objects.get(client=user)
    card = CreditCard.objects.get(account = account)