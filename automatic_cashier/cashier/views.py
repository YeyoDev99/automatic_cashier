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


@login_required(login_url='cashier:index')
def card_activation(request):
    if request.method == 'POST':
        form = CardActivation(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            account = Account.objects.get(client=request.user)
            card.account = account
            card.save()
            return redirect('cashier:menu') 
        else:
            messages.error(request, f'your credit card password is already been used by another account, please use another')      
    form = CardActivation()
    context = {
        'form': form
    }
    return render(request, 'cashier/card_activation.html', context)


@login_required(login_url='cashier:index')
def menu(request):
    user = request.user
    account = Account.objects.get(client=user)
    card = CreditCard.objects.get(account = account)
    context = {}
    if card.activation == False:
        messages = [f'your credit card is blocked']
        context.update({'messages': messages})
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
def card_validation(request, trans, tries):
    user = request.user
    account = Account.objects.get(client=user)
    card = CreditCard.objects.get(account = account)
    context = {}
    # task for new session: fix the try loop problem
    if card.activation == False:
        e_messages = [f'sorry, your credit card is blocked']
        context = {
            'messages': e_messages
        }
        return render(request, 'cashier/menu.html', context)

    if request.method == 'POST':
        if request.GET.get('q') == 'deposit_money':
            money = request.POST['money']
            if (float(money) > account.balance) and request.user.email != request.POST['user']:
                messages = [f'insufficient balance to complete the transaction']
                context = {
                    'messages': messages
                }
                return render(request, 'cashier/deposit.html', context)
            else:
                username = request.POST['user']
                user = User.objects.get(email=username)
                account = Account.objects.get(client=user)
                context.update({'account': account.pk, 'money': money})

        elif request.GET.get('q') == 'purchase_tickets':
            tickets = request.POST['tickets']
            money = float(tickets)*10000
            if float(money) > account.balance:
                messages = [f'insufficient balance to complete the transaction']
                context = {
                    'messages': messages
                }
                return render(request, 'cashier/purchase_tickets.html', context)
            else:
                context.update({'tickets': tickets})
        elif request.GET.get('q') == 'withdraw_money':
            money = request.POST['money']
            if float(money) > account.balance:
                messages = [f'insufficient balance to complete the transaction']
                context = {
                    'messages': messages
                }
                return render(request, 'cashier/withdraw_money.html', context)
            else:
                context.update({'money_withdraw': money})

        else:
            if card.password == request.POST['card-password']:
                if trans == 1:
                    return redirect('cashier:check_balance')
                elif trans == 2:
                    tickets = int(request.POST.get('tickets'))
                    money = tickets*10000
                    request_account= Account.objects.get(client=request.user)
                    request_account.balance -= money
                    request_account.save()
                    s_messages = [f'your transaction has been successful']
                    context = {
                    's_messages': s_messages
                    }
                    return render(request, 'cashier/menu.html', context)

                elif trans == 3:
                    money = float(request.POST.get('money'))
                    request_account= Account.objects.get(client=request.user)
                    account = request.POST.get('account')
                    account = Account.objects.get(pk=int(account))
                    if request_account != account:
                        request_account.balance -= money
                        request_account.save()
                    account.balance += money
                    account.save()                
                    s_messages = [f'your transaction has been successful']
                    context = {
                    's_messages': s_messages
                    }
                    return render(request, 'cashier/menu.html', context)

                elif trans == 4:
                    money = float(request.POST.get('money'))
                    request_account= Account.objects.get(client=request.user)
                    request_account.balance -= money
                    request_account.save()
                    s_messages = [f'your transaction has been successful']
                    context = {
                    's_messages': s_messages
                    }
                    return render(request, 'cashier/menu.html', context)
    
            else:
                tries += 1
                if tries == card.id_limit:
                    card.activation=False
                    card.save()
                    messages = [f'wrong password, your credit card has been blocked']
                    context = {
                        'messages': messages
                    }
                    return render(request, 'cashier/menu.html', context)
                messages = [f'wrong password, you have {3-tries} tries left']
                context = {
                'trans': trans, 
                'tries': tries,
                'messages': messages
                    }
                return render(request, 'cashier/card_validation.html', context)
    context.update({
        'trans': trans, 
        'tries': tries,
        })
    return render(request, 'cashier/card_validation.html', context)


@login_required(login_url='cashier:index')
def deposit(request):
    context = {}
    return render(request, 'cashier/deposit.html', context)


@login_required(login_url='cashier:index')
def deposit_money(request):    
    context = {}
    if request.GET.get('q') == 'another_account':
        context.update({'another': 'another'})
    else:
        context.update({'self': 'self'})
    return render(request, 'cashier/deposit_money.html', context)


@login_required(login_url='cashier:index')
def purchase_tickets(request):
    context = {}
    return render(request, 'cashier/purchase_tickets.html', context)


@login_required(login_url='cashier:index')
def withdraw_money(request):
    context = {}
    return render(request, 'cashier/withdraw_money.html', context)
