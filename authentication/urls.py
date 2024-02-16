from django.urls import path

from authentication.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout', logout, name='logout' )

    # Add more URL patterns as needed
]
