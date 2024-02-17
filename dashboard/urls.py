# urls.py
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('update_profile/',update_profile, name='update_profile'),
    path('view_profile/', view_profile, name='view_profile'),
    path('search/', search, name="search"),
    path('search/profile/<str:reviewemail>','profile', name="profile"),
    path('search/reviewprofile/<str:reviewemail>','reviewprofile', name="reviewprofile")




    
    # ...
]
