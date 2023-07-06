from django.http import HttpResponse
from django.shortcuts import render
from account.models import User

def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        #print(user)

        return HttpResponse('Your account is activated. You can go ahead and login !')  
    
    else:
        return HttpResponse('The parameters is not valid')