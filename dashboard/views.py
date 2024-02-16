from django.shortcuts import render, HttpResponse
from authentication.logic import *
from authentication.logic import auth



# Create your views here.
@auth()
def dashboard (request):
    
    logic_token, user_email= get_session_data(request, "login_token")
    user_name = UserDetails.objects.get(email=user_email)

    print(user_name.name)
    print('1')
    return render(request, "navbar.html", {'user_name': user_name.name})


#Create your views here.

@auth(by_pass_route=True)
def update_profile(request):
    

    if request.method == "GET":        
        if request.user:
            return render(
                request,
                "update_profile.html",
                {
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about,
                    "review":request.user.review
                
                },
            )   
         
        messages.error(request, "You are not authorized to view this page.")
        return redirect("/dashboard")

    elif request.method == "POST":
        return update_profile_logic(request)


@auth(by_pass_route=True)

def update_profile_logic(request):
    print(request.method)
    print("update")
    if request.method == "POST":  # Corrected from "post" to "POST"
        data = {
            "name": request.POST.get("first-name"),
            "last-name": request.POST.get("last-name"),
            "location": request.POST.get("location"),  # Corrected from "loaction" to "location"
            "designation": request.POST.get("designation"),
            "skills": request.POST.get("skills"),
            "about": request.POST.get("about")


        }
        print('data')

        user = UserDetails.objects.get(email=request.user.email)
        user.name = data["name"]
        user.last_name = data["last-name"]
        user.location = data["location"]
        user.designation = data["designation"]
        user.skills = data["skills"]
        user.about= data["about"]
        user.save()
        messages.success(request, "Profile updated successfully.")
        print('dashboard')

        return redirect("/dashboard/")
    else:
        print('enterd esle')
    
    return render(request, "update_profile.html")

@auth(by_pass_route=True)
def view_profile(request):
    if request.method == "GET":
        

        if request.user:
            return render(
                request,
                "view_profile.html",
                {    
                    "email": request.user.email,
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about,
                    "review": request.user.review
                    # if request.user.date_of_birth
                    # else "",
                },
            )
         
        messages.error(request, "You are not authorized to view this page.")
        return redirect('/login/')
    
@auth()
def search(request):
    if request.method=='GET':
        query=request.GET.get("search-skills")
        print (query)
        if query:
            SearchResult=UserDetails.objects.filter(skills__contains=query)

            print(SearchResult)
            if SearchResult:
                result_data_list = []

                for users in SearchResult:

            
                    result_data = {
                    'email': users.email,
                    'name': users.name,
                    'last_name':users.last_name,
                    'designation': users.designation,
                    'skills': users.skills,
                    'location': users.location
            

                    }     
                    print(result_data)
                    result_data_list.append(result_data)

                # print(result_data_list)
                print ('search')
            else:
                messages.error(request, "No search found")
                print("not found")
                return redirect("/dashboard/")
        else:
            messages.error(request, "Nothing entered")
            print("Nothing entered")
            return redirect("/dashboard/")


    return render(request, 'search.html', { 'result_data_list' : result_data_list
    },
    )


@auth()
def profile(request,email):
    if request.method=='GET':
        reviewbox= request.GET.get("review-box")

        user = UserDetails.objects.get(email=email)
        user.review = reviewbox
        user.save()
        print(user.review)
        print('yyy')
    
    user = UserDetails.objects.get(email=email)
    data = {
        "email" : user.email,
        "name":user.name,
        "last_name":user.last_name,
        'designation': user.designation,
        'skills': user.skills,
        'location': user.location,
        'about':user.about, 
        'review':user.review
        
    }
    print('data')

    

    return render(request, 'profile.html',{ 'data' : data,  
     },)
    


    

