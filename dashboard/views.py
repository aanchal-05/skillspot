from django.shortcuts import render, HttpResponse
from authentication.logic import *
from authentication.logic import auth
from dashboard.models import Review
from authentication.models import UserDetails
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Avg






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
            user_being_reviewed = Review.objects.filter(user_being_reviewed_id=request.user.email)
            if(user_being_reviewed):
                print(user_being_reviewed)
                review_data_list = []

                for reviews in user_being_reviewed:

            
                    review_data = {
                    'content': reviews.content,
                    'reviewer': reviews.reviewer.email,

                    'user_being_reviewed': reviews.user_being_reviewed.email


                }   
                    review_data_list.append(review_data) 
                print(review_data_list) 
                return render(request, "view_profile.html", {'review_data_list': review_data_list,  "email": request.user.email,
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about})
            
            
            
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
                    # "review": request.user.review
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
def profile(request,reviewemail):
   
    user_being_reviewed = UserDetails.objects.get(email=reviewemail)
    user = UserDetails.objects.get(email=reviewemail)
    print(user)
    data = {
        "email" : user.email,
        "name":user.name,
        "last_name":user.last_name,
        'designation': user.designation,
        'skills': user.skills,
        'location': user.location,
        'about':user.about, 
       
        
    }
    rate = request.GET.get('rate', None)
    print(rate, "rate")
    if(rate):
        review1=Review(
            rating=rate,
            reviewer=request.user,  # Set reviewer to the user giving the review
            user_being_reviewed=user_being_reviewed
        )
        review1.save()
    # user_detail = UserDetails.objects.all()
    # for user in user_detail:

    avg_rating = Review.objects.filter(user_being_reviewed_id=reviewemail).aggregate(Avg('rating'))['rating__avg'] or 0.0
    print(avg_rating)
    user.avgrating=avg_rating
    user.save()
    print(user)

    if request.method=='POST':
        reviewbox= request.POST.get("review-box")
        if reviewbox:
            # user = UserDetails.objects.get(email=email)
            review = Review(
                content=reviewbox,
                reviewer=request.user,  # Set reviewer to the user giving the review
                user_being_reviewed=user_being_reviewed
            )
            review.save()
            print('yyy')
        else:
            print('else')

    else:
        print('else entered')
   
    reviewuser=Review.objects.filter(user_being_reviewed_id=reviewemail)
    print(reviewuser)
    if reviewuser:
        result_review_user = []

        for users in reviewuser:

            
            result_review_data = {
                'content': users.content,
                'reviewer': users.reviewer.email,

                'user_being_reviewed': users.user_being_reviewed.email,
                # 'rating':users.rating


                }     
            result_review_user.append(result_review_data)
        print('###')
        print(result_review_user)
        # print(result_review_user[0]['reviewer'].email)

        print('###')
        # print(result_review_user)
        return render(request, 'profile.html',{ 'data' : data,  'result_review_user' : result_review_user
     },)
    
    else:
         print('no review')
    
    return render(request, 'profile.html',{ 'data' : data})



# views.py
def rate(request,reviewemail, rate):
    return HttpResponse("hi")


# @require_POST
# def rate_post(request, post_id):
#     try:
#         rating = int(request.POST.get('rating', 0))
#         # Ensure the rating is within a valid range (e.g., 1 to 5)
#         rating = max(1, min(5, rating))

#         # Assuming 'post_id' is the ID of the post you're rating
#         post = Review.objects.get(id=post_id)
#         post.rating = rating
#         post.save()

#         response_data = {'success': True, 'message': 'Rating updated successfully'}
#     except Exception as e:
#         response_data = {'success': False, 'message': str(e)}

#     return JsonResponse(response_data)
