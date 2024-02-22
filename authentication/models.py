from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
import os
from django.core.exceptions import ValidationError





# Create your models here.


# Create your models here.
def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Only JPG and PNG images are allowed.")
    
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
    review= models.CharField(max_length=1000,blank=True, null=True)
    avgrating= models.FloatField(default=0)
    image = models.ImageField(
        blank=True,
        null=True
        # validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )




    
