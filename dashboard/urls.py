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
    path('search/profile/<str:reviewemail>', reviewprofile, name="profile"),
    path('search/profile/rating/<str:reviewemail>', rating, name="rating"),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
