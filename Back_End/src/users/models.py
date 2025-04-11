from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser , PermissionsMixin

from django.core.exceptions import ValidationError


from tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields


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


def user_image_upload_path(instance, filename):
    if not instance.id:
        # Handle case where instance isn't saved yet
        return f'Users/temp/{filename}'
    return f'Users/{instance.id}/{filename}'
class User(AbstractBaseUser , PermissionsMixin , TimeStampedModel):
    class Meta:
        db_table = 'users'
    fullname = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(null=True,blank=True , upload_to=user_image_upload_path) #TODO put default photo
    
    #TODO Tasks (if needed)

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
    

