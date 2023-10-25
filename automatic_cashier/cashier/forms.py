from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, CreditCard
from django import forms

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label= "Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password','placeholder':'password', 'id': 'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'placeholder':'password'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','cellphone','direction','password1', 'password2']
        widgets= {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write your last name'}),

            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'write your email'}),
            'direction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write your direction'}),
            'cellphone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write a valid cellphone'}),
        }

class CardActivation(ModelForm):
    password = forms.CharField(
        label= "Credit Card Password Set Up",
        widget=forms.PasswordInput(attrs={'class':'form-control password', 'type':'password','placeholder':'####', 'id': 'password', 'maxlength': '4'}),
    )       
    class Meta:
        model = CreditCard
        fields = ['password']