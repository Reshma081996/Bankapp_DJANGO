from django.core.checks import messages
from django.db import models 
from django.forms import ModelForm, fields, widgets
from django.forms.forms import Form
from .models import Account, CustomUser,Transactions

from django import forms


class UserRegistrationForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control"}))

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "age", "phone"]
        widgets={
            'username':forms.TextInput(attrs={'class':"form-control"}),
            'email':forms.TextInput(attrs={'class':"form-control"}),
            'age':forms.TextInput(attrs={'class':"form-control"}),
            'phone':forms.TextInput(attrs={'class':"form-control"})
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))


class CreateAccount(ModelForm): 
    class Meta:
        model = Account
        fields = ["account_number", "balance",
                  "ac_type", "user", "active_status"]
       
        widgets={
            'account_number':forms.TextInput(attrs={'class':"form-control"}),
            'balance':forms.TextInput(attrs={'class':"form-control"}),
            'ac_type':forms.TextInput(attrs={'class':"form-control"}),
            'user':forms.TextInput(attrs={'class':"form-control"}),
            'active_status':forms.TextInput(attrs={'class':"form-control"})
        }

class TransactionCreateForm(forms.Form):
    #model=Transactions()
    user = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    to_account_number = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control"}))
    confirm_account = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    amount = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        to_account_number = cleaned_data.get('to_account_number')
        confirm_account = cleaned_data.get('confirm_account')
        amount = int(cleaned_data.get('amount'))
        user = cleaned_data.get('user')
        print(to_account_number, amount, user)

        try:  # if  toaccount exist in account model
            account = Account.objects.get(account_number=to_account_number)

        except:
            msg = "Invalid account number"
            self.add_error("to_account_number", msg)

        if to_account_number != confirm_account:  # to acc and confirm acc same ano en ariyam
            msg = "account number mismatch"
            self.add_error("to_account_number", msg)

        # current user balance

        # user(left) expecting id but right user is str. so we use __username
        account = Account.objects.get(user__username=user)
        # i.e account->userof custom user-> user__username
        aval_bal = account.balance
        if amount > aval_bal:
            message = "insufficient balance"
            self.add_error("amount", message)
