from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]

        if password == repeat_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already exist")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username already exist")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                return redirect("login")
        else:
            messages.info(request, "password not the same")
            return redirect("register")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "credentials not correct")
            return redirect("login")

    return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect("/")