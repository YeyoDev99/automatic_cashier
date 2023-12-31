from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    direction = models.TextField(default="not apply")
    cellphone = models.CharField(max_length=10, default='not apply')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password', 'password2']

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 


class Account(models.Model):
    balance = models.FloatField(default=999999.99)
    opening_date = models.DateField(auto_now_add=True)
    client = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.client} account'

    def show_balance(self):
        return self.balance


class CreditCard(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, default=1)
    password = models.CharField(max_length=4, unique=True)
    id_limit  = models.IntegerField(default=3)        
    activation = models.BooleanField(default=True)

    def block_credit_card(self):
        self.activation = False

class Cashier(models.Model):
    location = models.CharField(max_length=100, default="not apply")
    available_balance = models.FloatField()
    affiliated_bank = models.CharField(max_length=100, default="bank")
    max_withdrawal_amount = models.FloatField() 
    CreditCards = models.ManyToManyField(CreditCard, related_name="credit_cards")    


