from django.shortcuts import render
from django.contrib import messages
from authentication.models import UserDetails
from authentication.logic import *
from . import logic
from django.shortcuts import redirect
from .utils import get_or_none


def login(request):
    
    if request.method == "POST":
        email = request.POST["login-email"]
        password = request.POST["login-password"]

        if not (password and email):
            messages.error(request, "Fields cannot be empty")
            return redirect("/login/")
        
        # Use get_or_none to retrieve user details or None if not found

        userdetail = get_or_none(UserDetails, email=email, password=logic.hash_password(password))


        if userdetail:
            # Set session data upon successful login
            logic.set_session_data(request, "login_token", userdetail.email)
            messages.success(request, "Logged in successfully")
            return redirect("/dashboard/")
        
        else:
            messages.error(request, "Inavlid Credentials")
            return redirect("/login/")
        
    return render(request, 'login.html')


def signup(request):

    if request.method == "POST":
        # Extracting data from the POST request
        email = request.POST.get('signup-email')
        name = request.POST.get("signup-username")
        password = request.POST.get("signup-password")
        repass = request.POST.get("signup-re-password")
        
        # Validating input fields
        if not (password and email and repass):
                messages.error(request, "Fields cannot be empty")
                return redirect("/signup/")

        if not password == repass:
                messages.error(request, "Password does not match re-entered password")
                return redirect("/signup/")
        
        if not is_valid_password(password):
            messages.error(request, "Password should be at least 8 characters, contain at least one special character, and have at least one uppercase letter")
            return redirect("/signup/")
        
        # Checking if the user already exists

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "You are already registered... please login again")
            return redirect("/login/")
        
        # Creating a new user and saving to the database

        UserDetails(email=email, name=name, password=logic.hash_password(password)).save()

        # Setting session data for the registered user

        logic.set_session_data(request, "login_token", email )
        messages.success(request, "You are registered now.....please login")
        return redirect("/login/")
        
    return render(request, 'signup.html')




@logic.auth()
def logout(request):
    #delete session
    logic.delete_session_data(request, "login_token")
    messages.success(request, "Logged out successfully")
    return redirect("/login/")
