from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin
# from django.contrib.auth.hashers import make_password , check_password

from django.core.exceptions import ValidationError


from src.Tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self , fullname , email , password = None , **extra_fields):
        if not fullname:
            raise ValueError('user Must have fullname')
        if not email:
            raise ValueError('user must have an email')
        email = self.normalize_email(email)
        user = self.model(fullname = fullname , email = email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, fullname , email , password , **extra_fields):
        extra_fields.setdefault('is_staff' , True)
        extra_fields.setdefault('is_superuser' , True)
        extra_fields.setdefault('is_active' , True)

        return self.create_user(fullname , email , password , **extra_fields)



class User(AbstractBaseUser , PermissionsMixin , TimeStampedModel):
    class Meta:
        app_label = 'Users'
        db_table = 'users'
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image = models.ImageField(null=True,blank=True , upload_to=f'Users/{id}/') #TODO put default photo

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager() # connect this class to the CustomUserManager

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # Important to avoid reverse name clashes
        related_query_name="user",
    )

    def __str__(self):
        return self.fullname
    

