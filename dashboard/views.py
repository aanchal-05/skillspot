from django.shortcuts import render, HttpResponse
from authentication.logic import *
from authentication.logic import auth
from dashboard.models import Review
from authentication.models import UserDetails

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
        #if user authenticated    
        if request.user:
            return render(request,"update_profile.html",{
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about,
                    "review":request.user.review,
                },)
         
        messages.error(request, "You are not authorized to view this page.")
        return redirect("/dashboard")

    elif request.method == "POST":
        return update_profile_logic(request)



@auth(by_pass_route=True)
def update_profile_logic(request):

    if request.method == "POST": 
        #fetch data
        data = {
            "name": request.POST.get("first-name"),
            "last-name": request.POST.get("last-name"),
            "location": request.POST.get("location"), 
            "designation": request.POST.get("designation"),
            "skills": request.POST.get("skills"),
            "about": request.POST.get("about"),
        }
        
        # check if any field is empty  
        for value in data.values():
             if not value:
                messages.error(request, "Fields cannot be empty")
                return redirect("/update_profile/")   
        
        #save data
        user = UserDetails.objects.get(email=request.user.email)
        # print(name)
        print(user.name)
        user.name = data["name"]
        user.last_name = data["last-name"]
        user.location = data["location"]
        user.designation = data["designation"]
        user.skills = data["skills"]
        user.about= data["about"]
        user.save()
        
        messages.success(request, "Profile updated successfully.")
        return redirect("/dashboard/")
    
    
    return render(request, "update_profile.html")

@auth(by_pass_route=True)
def view_profile(request):

    # Check if the user is authenticated
 
    if request.user:

        # Fetch review details from the Review table for the logged-in user

        user_being_reviewed = Review.objects.filter(user_being_reviewed_id=request.user.email)
        # Check if any reviews were found for logged in-user

        if user_being_reviewed:
            review_data_list = []
            # Iterate through the reviews for the logged-in user

            for reviews in user_being_reviewed:
                review_data = {
                    'content': reviews.content,
                    'reviewer': reviews.reviewer.email,
                    'user_being_reviewed': reviews.user_being_reviewed.email
            }   
            review_data_list.append(review_data) 
                
            # Render the view_profile.html template with review data and user details
    
            return render(request, "view_profile.html", {'review_data_list': review_data_list,  "email": request.user.email,
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about,
                    "avgrating":request.user.avgrating, 
                 })
            
        # If no reviews were found, render the template with user details only

        return render(request,"view_profile.html",{    
                    "email": request.user.email,
                    "name": request.user.name,
                    "last_name": request.user.last_name,
                    "location": request.user.location,
                    "skills": request.user.skills,
                    "designation": request.user.designation,
                    "about": request.user.about,
                    "avgrating":request.user.avgrating,
                    },)
             # If the user is not authenticated, display an error message
      
    messages.error(request, "You are not authorized to view this page.")
    return redirect('/login/')

    
@auth()
def search(request):
    if request.method=='GET':

        search_box=request.GET.get("search-skills")

        # Check if the searchbox is empty

        if not search_box:
            messages.error(request, "You entered nothing in search-box")
            return redirect("/dashboard/")
        
        # Filter the UserDetails based on the search query

        SearchResult=UserDetails.objects.filter(skills__contains=search_box)

        # Check if any results were found

        if not SearchResult:
            messages.error(request, "No result found")
            return redirect("/dashboard/")
        
        # Create a list of dictionaries containing the search results

        result_data_list = []

        for users in SearchResult:
            result_data = {
            'email': users.email,
            'name': users.name,
            'last_name':users.last_name,
            'designation': users.designation,
            'skills': users.skills,
            'location': users.location,
            'avgrating':users.avgrating
            }           
            
            result_data_list.append(result_data)
               
    return render(request, 'search.html', { 'result_data_list' : result_data_list, 'user_name':request.user.name
    },
    )



# @auth()
# def reviewprofile(request,reviewemail):
   
#     user_being_reviewed = UserDetails.objects.get(email=reviewemail)
    
#     data = {
#         "email" : user_being_reviewed.email,
#         "name":user_being_reviewed.name,
#         "last_name":user_being_reviewed.last_name,
#         'designation': user_being_reviewed.designation,
#         'skills': user_being_reviewed.skills,
#         'location': user_being_reviewed.location,
#         'about':user_being_reviewed.about,
#         'avgrating':user_being_reviewed.avgrating
#      }
#     rate = request.GET.get('rate', None)
#     # # print(rate, "rate")
#     # if(rate):
#     #     review1=Review(
#     #         rating=rate,
#     #         reviewer=request.user,  # Set reviewer to the user giving the review
#     #         user_being_reviewed=user_being_reviewed
#     #     )
#     #     review1.save()
    

#     # avg_rating = Review.objects.filter(user_being_reviewed_id=reviewemail).aggregate(Avg('rating'))['rating__avg'] or 0.0
#     # print(avg_rating)
#     # user.avgrating=avg_rating
#     # user.save()
#     # print(user.avgrating)


#     if request.method=='POST':
#         reviewbox= request.POST.get("review-box")
#         if reviewbox:
#             review = Review(
#                 content=reviewbox,
#                 reviewer=request.user, 
#                 user_being_reviewed=user_being_reviewed
#             )
#             review.save()
#             print('yyy')
#         else:
#             print('else')

#     else:
#         print('else entered')
   
#     reviewuser=Review.objects.filter(user_being_reviewed_id=reviewemail)
#     print(reviewuser)
#     if reviewuser:
#         result_review_user = []

#         for users in reviewuser:

            
#             result_review_data = {
#                 'content': users.content,
#                 'reviewer': users.reviewer.email,

#                 'user_being_reviewed': users.user_being_reviewed.email,


#                 }     
#             result_review_user.append(result_review_data)
#         print('###')
#         print(result_review_user)

#         print('###')
#         return render(request, 'profile.html',{ 'data' : data,  'result_review_user' : result_review_user , 'user_name':request.user.name
#      },)
    
#     else:
#          print('no review')
    
#     return render(request, 'profile.html',{ 'data' : data, 'user_name' :request.user.name, 'avgrating': avg_rating})

# @auth(by_pass_route=True)
# def rating (request, reviewemail):
#     user_being_reviewed = UserDetails.objects.get(email=reviewemail)
#     rate = request.GET.get('rate', None)
#     # print(rate, "rate")
#     if(rate):
#         review1=Review(
#             rating=rate,
#             reviewer=request.user,  # Set reviewer to the user giving the review
#             user_being_reviewed=user_being_reviewed
#         )
#         review1.save()
    

#         avg_rating = Review.objects.filter(user_being_reviewed_id=reviewemail).aggregate(Avg('rating'))['rating__avg'] or 0.0
#         print(avg_rating)
#         user_being_reviewed .avgrating=avg_rating
#         user_being_reviewed.save()
#         return render (request, 'profile.html')
#         # view_profile(reviewemail)



#     #     data = {
#     #     "email" : user_being_reviewed.email,
#     #     "name":user_being_reviewed.name,
#     #     "last_name":user_being_reviewed.last_name,
#     #     'designation': user_being_reviewed.designation,
#     #     'skills': user_being_reviewed.skills,
#     #     'location': user_being_reviewed.location,
#     #     'about':user_being_reviewed.about, 
#     #     'avgrating':user_being_reviewed.avgrating
#     #  }
#     #     return render(request, 'profile.html',{ 'data' : data, 'user_name' :request.user.name, })
    
#     else:
#         messages.error(request, "No ratinng given by you.")
#         return redirect("/profile")




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
        'about':user.about
    
       
        
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
    

    avg_rating = Review.objects.filter(user_being_reviewed_id=reviewemail).aggregate(Avg('rating'))['rating__avg'] or 0.0
    print(avg_rating)
    user.avgrating=avg_rating
    user.save()
    print(user.avgrating)


    if request.method=='POST':
        reviewbox= request.POST.get("review-box")
        if reviewbox:
            review = Review(
                content=reviewbox,
                reviewer=request.user, 
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


                }     
            result_review_user.append(result_review_data)
        print('###')
        print(result_review_user)

        print('###')
        return render(request, 'profile.html',{ 'data' : data,  'result_review_user' : result_review_user , 'user_name':request.user.name, 'avgrating': avg_rating
     },)
    
    else:
         print('no review')
    
    return render(request, 'profile.html',{ 'data' : data, 'user_name' :request.user.name, 'avgrating': avg_rating})




   


