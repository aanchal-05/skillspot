from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # Add more URL patterns as needed
]
