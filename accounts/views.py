from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,'User with this username already exists')
            return redirect("/register/")
        
        user = User.objects.create_user(username=username)

        user.set_password(password)

        user.save()
        
        messages.info(request,'User created successfully')
        return redirect('/login/')
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context,request))
    
    

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'User with this username does not exist')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request,'invalid password')
            return redirect('/login')
        

        login(request,user)
        messages.info(request,'login successful')

        return redirect('/dashboard/')
    
    template = loader.get_template('login.html')
    context ={}
    return HttpResponse(template.render(context,request))

def logout_user(request):
    logout(request)
    messages.info(request,'logout successful')
    return redirect('/login/')

# Dashboard view

#@login_required  # This ensures only logged-in users can access the dashboard
def dashboard_view(request):
    template = loader.get_template('dashboard.html')
    context = {}
    return HttpResponse(template.render(context,request))