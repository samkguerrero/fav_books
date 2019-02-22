from django.shortcuts import render, redirect
from .models import *
# from time import strftime, gmtime
# from dateutil import parser
from django.contrib import messages
import bcrypt

def index(request):
    if 'logged_in_user' in request.session:
        return redirect("/books")
    else:
        return render(request, "log_reg/index.html") 

def process(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
            return redirect("/")
        else:
            new_user = User.objects.create(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                email = request.POST['email'],
                password = bcrypt.hashpw( request.POST['password'].encode(), bcrypt.gensalt())
            )
            request.session['logged_in_user'] = request.POST['fname']
            request.session['logged_in_user_id'] = new_user.id
            request.session['log_reg'] = 'registered'
            return redirect("/success")

def success(request):
    if not 'logged_in_user' in request.session:
        return redirect("/")
    else:
        return render(request, "log_reg/success.html") 

def logout(request):
    request.session.flush()
    return redirect("/")

def login(request):
    if request.method == "POST":
        login_errors = User.objects.login_validator(request.POST)
        if len(login_errors):
            for tag, error in login_errors.items():
                messages.error(request, error, extra_tags=tag)
            return redirect("/")
        else:
            user_logged_in = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), user_logged_in.password.encode()):
                request.session['logged_in_user'] = user_logged_in.first_name
                request.session['logged_in_user_id'] = user_logged_in.id
                request.session['log_reg'] = 'logged in'
                return redirect("/")
            else:
                return redirect("/")