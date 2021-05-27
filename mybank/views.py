import django
from django.db import models
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.forms import forms
from django.contrib.auth import authenticate, get_user, login as djangologin

# Create your views here.
from .forms import UserRegistrationForm, UserLoginForm, CreateAccount,TransactionCreateForm
from .models import CustomUser, Account,Transactions

from django.views.generic import TemplateView

#importing decorators for validation
from django.utils.decorators import method_decorator
from .decorators import account_created_validator

def base(request):
   return render(request,"base.html")

def index(request):
    context={}
    try:
     # check for login account status= active
        account = Account.objects.get(user=request.user)
        status = account.active_status
        print(status)
        flag = True if status == "active" else False
        context["flag"] = flag
        return render(request, "home.html", context)
    except:
        return render(request,"home.html",context)




class Registration(TemplateView):
    model=CustomUser
    form_class=UserRegistrationForm
    template_name="register.html"
    context={}
    def get(self, request, *args, **kwargs) :
        self.context['form']=self.form_class()
        return render(request,self.template_name,self.context) 
    def post(self,request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"login.html")
        else:       
            self.context['form']=self.form_class()
            return render(request,self.template_name,self.context)



class  LoginView(TemplateView):
    model=CustomUser
    template_name="login.html"
    form_class = UserLoginForm
    context = {}
    def get(self, request, *args, **kwargs):
       self.context['form']=self.form_class()
       return render(request,self.template_name,self.context)

       
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print(username,password)
            user=self.model.objects.get(username=username)
            print(user)
            if ((user.username==username) and (user.password==password)):
                djangologin(request,user)
                print("success")
                return redirect("index")
                # try:
                # #check for login account status= active
                #     account=Account.objects.get(user=request.user)
                #     status=account.active_status
                #     print(status)
                #     flag=True if status=="active" else False
                #     self.context["flag"]=flag
                #     return render(request,"home.html",self.context)
                # except:
                #     return render(request,"home.html",self.context)
            else:
                print("failed")
                return render(request,self.template_name,self.context)


@method_decorator(account_created_validator,name="dispatch")
class AccountCreateView(TemplateView):
    model=Account
    form_class=CreateAccount
    template_name="create_acc.html"
    context={}
    def get(self, request, *args, **kwargs) :
        # sbk-1000
        # last created acc+1 sbk-1001
        account_number=""
        account= self.model.objects.all().last() #fetch last account
        if account:
            acno=int(account.account_number.split("-")[1])+1 #[sbk,1000]
            print(acno)
            account_number="sbk-"+str(acno)
            print(account_number)
        else:
            account_number="sbk-1000"
        self.context['form']=self.form_class(initial={"account_number":account_number,"user":request.user})
        return render(request,self.template_name,self.context)

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

        else:

            self.context['form']=self.form
            return render (request,self.template_name,self.context)

  
 # update mybank_account set active_status="active" where id = 2




class GetUserMixin(object):
    def get_user(self,account_num):
        return Account.objects.get(account_number=account_num)


class  Transactionsview(TemplateView,GetUserMixin):
    model=Transactions
    template_name="transactions.html"
    form_class=TransactionCreateForm
    context={}
    def get(self, request, *args, **kwargs):
       self.context['form']=self.form_class(initial={"user":request.user})
       return render(request,self.template_name,self.context)

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
           to_account=form.cleaned_data.get("to_account_number") # fetch toaccount , amount
           amount=form.cleaned_data.get("amount")
           remarks=form.cleaned_data.get("remarks")
           account=self.get_user(to_account) #calling get_user of GetUserMixin
           account.balance+=int(amount)
           account.save()
           cur_acct=Account.objects.get(user=request.user)
           cur_acct.balance-=int(amount)
           cur_acct.save()
           #no modal form used form.save()
           #instead create obj for transaction model and passing values to appropriatefields as per model
            # user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
            # amount=models.IntegerField()
            # to_accno=models.CharField(max_length=12)
            # date=models.DateField(auto_now=True)
            # remarks=models.CharField(max_length=12)
           transaction=Transactions(user=request.user,amount=amount,to_accno=to_account,remarks=remarks)
           transaction.save() # every transaction appear on transaction_table
           return redirect("index")



        else:
            self.context['form']=form
            return render(request,self.template_name,self.context)

class  BalanceEnquiry(TemplateView):
    def get(self, request, *args, **kwargs):
        account=Account.objects.get(user=request.user)
        balance=account.balance
        return render(request,"balance.html",{"balance":balance})
        # return JsonResponse({"balance":balance})




class TransactionHistory(TemplateView):
    def get(self, request, *args, **kwargs):
        debit_transactions=Transactions.objects.filter(user=request.user)
        l_user=Account.objects.get(user=request.user)
        credit_transactions=Transactions.objects.filter(to_accno=l_user.account_number)
        return render(request,"transactionhistory.html",{"dtransactions":debit_transactions,"ctransactions":credit_transactions})




 