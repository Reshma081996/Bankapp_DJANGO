from .models import Account
from  django.shortcuts import redirect
from  django.contrib import messages

def account_created_validator(func):
    def wrapper(request,*args,**kwargs):
        try: # if there is a user who dont hav acount , query mismatching error occurs, to avoid that use try except block 
            account=Account.objects.get(user=request.user)
            status=account.active_status
            if status=="active" :
                messages.error(request,"account already created for this user")
                return redirect("index")
            else:
                return func(request,*args,**kwargs)
        except:
            return func(request,*args,**kwargs)
    return wrapper