from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from authentication.models import UserDetails
from authentication.logic import *
from . import logic
from django.shortcuts import redirect


def login(request):
  
    
    # if logic.get_session_data(request, "login_token"):
    #      return redirect("/dashboard/")

    if request.method == "POST":
        email = request.POST["login-email"]
        password = request.POST["login-password"]

        if not (password and email):
            messages.error(request, "Fields cannot be empty")
            return redirect("/login/")
        
        userdetail = UserDetails.objects.filter(email=email).filter(password=logic.hash_password(password)).first()
        
        print(userdetail)
        

        if userdetail:
            
        
            print(userdetail.name)

            logic.set_session_data(request, "login_token", userdetail.email)
            messages.success(request, "Logged in successfully")
            return redirect("/dashboard/")
        else:
            print('invalid')
            messages.error(request, "Inavlid Credentials")
            return redirect("/login/")
    return render(request, 'login.html')


def signup(request):
    
    print(request.method)

    if request.method == "POST":
      print('11')
      email = request.POST.get('signup-email')
      name = request.POST.get("signup-username")
      password = request.POST.get("signup-password")
      repass = request.POST.get("signup-re-password")
      print(name)
    
      if not (password and email and repass):
            messages.error(request, "Fields cannot be empty")
            return redirect("/signup/")

      if not password == repass:
            messages.error(request, "Password does not match re-entered password")
            return redirect("/signup/")

      if UserDetails.objects.filter(email=email).exists():
          messages.error(request, "You are already registered... please login again")
          return redirect("/login/")
      UserDetails(email=email, name=name, password=logic.hash_password(password)).save()

      #UserDetails(email=email, password=password, name=name).save()
      logic.set_session_data(request, "login_token", name)
      messages.success(request, "You are registered now.....please login")
      return redirect("/login/")
    
    return render(request, 'signup.html')




@logic.auth()
def logout(request):
    logic.delete_session_data(request, "login_token")
    messages.success(request, "Logged out successfully")
    return redirect("/login/")
