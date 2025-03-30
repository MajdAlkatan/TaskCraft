from django.db import models
from Users.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    startDate = models.DateTimeField(auto_now_add=False)
    user_id = models.ForeignKey(User , models.CASCADE)
    image = models.ImageField(null = True)


class user_task(models.Model):
    user_id = models.ForeignKey(User , models.CASCADE)
    task_id = models.ForeignKey(Task , models.CASCADE)
    
# Create your models here.
