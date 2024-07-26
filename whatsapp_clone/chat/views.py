from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request,'index.html',context={'users':users})

def chatPage(request,username):
    user_obj=User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    return render(request,'main_chat.html',context={'users':users,'user':user_obj})

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'{username}, You are logged in.')
            return redirect('home')
        else:
            messages.info(request, 'Wrong passwrod or username')
            return redirect('user_login')
    return render(request, 'login.html')
