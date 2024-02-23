"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import *
from dashboard.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('dashboard/',dashboard, name="dashboard"),
    path('logout/' ,logout, name="logout"),
    path('update_profile/', update_profile ,name="update_profile"),
    path('view_profile/', view_profile, name="view_profile"),
    path('search/', search, name="search"),
    path('search/profile/<str:reviewemail>', reviewprofile, name="profile"),
    path('search/profile/rating/<str:reviewemail>', rating, name="rating")

    # path('rate/<str:reviewemail>/<int:rate>/',rate, name"rate")

    # path('search/reviewprofile/<str:reviewemail>', reviewprofile, name="reviewprofile")




]
