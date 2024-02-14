from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.


# Create your models here.
class UserDetails(models.Model):
    email = models.EmailField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)


    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    designation= models.CharField(max_length=255 ,blank=True, null=True)
    skills= models.CharField(max_length=1000,blank=True, null=True)
    # about= models.TextField(blank=True, null=True)
    about= RichTextField(blank=True, null=True)


    
