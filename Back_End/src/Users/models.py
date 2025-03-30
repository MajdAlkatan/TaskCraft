from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password , check_password

from django.core.exceptions import ValidationError


from src.Tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields

# Create your models here.

class User(TimeStampedModel):
    class Meta:
        app_label = 'Users'
        db_table = 'users'
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100) #TODO search about hashing the password
    image = models.ImageField(null=True,blank=True , upload_to=f'Users/{id}/') #TODO put default photo

    def __str__(self):
        return self.fullname
    
    def validate_password(self , password):
        return check_password(password , self.password)
    def hash_password(self , password):
        return make_password(password)
    def save(self, *args , **kwargs):
        return super().save(*args , **kwargs)
    def delete(self, *args , **kwargs):
        return super().delete(*args , **kwargs)
    