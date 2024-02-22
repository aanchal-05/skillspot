# urls.py
from django.urls import path
from dashboard.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('update_profile/', update_profile, name='update_profile'),
    path('view_profile/', view_profile, name='view_profile'),
    path('search/', search, name="search"),
    path('search/profile/<str:reviewemail>', profile, name="profile"),
    # path('search/reviewprofile/<str:reviewemail>','reviewprofile', name="reviewprofile")
    # path('rate/<str:reviewemail>/<int:rate>/',rate, name"rate")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
