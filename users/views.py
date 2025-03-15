from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Users
from cryptography.models import EncryptedFile

def logout(request):
    auth.logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('index')


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(request,
                                 username=request.POST['email'], 
                                 password=request.POST['password'])
                       
        if user is None:
            messages.error(request, 'Invalid Credentials. Please signup first.')
            return redirect('login')
        else:
            auth.login(request, user)
            messages.success(request,'Login successful')
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('index')
    else:
        return render(request, 'users/login.html')


def signup(request):
    if request.method=='POST':
        try:
            user=User.objects.get(username=request.POST['email'])
            messages.success(request,'user exists already')
            return redirect('signup')

        except User.DoesNotExist:
            user=User.objects.create_user(username=request.POST['email'],password=request.POST['password'])
            newuser=Users.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'],
            )

            auth.login(request,user)
            messages.success(request,'Signup successful')
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('index')

    else:
        return render(request,'users/signup.html',{
            "users":list(User.objects.values_list('username',flat=True))
        })
