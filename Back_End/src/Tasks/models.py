from django.db import models
from Users.models import User
from Tools.tools import TimeStampedModel

class Task(TimeStampedModel):
    class Meta:
        app_lebal = "Tasks"
        db_table = "tasks"
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000 , default= "There is no description")
    startDate = models.DateField(auto_now_add=False)
    owner_id = models.ForeignKey(User , name= 'user_id', on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True , upload_to=f'Users/{id}/')
    users = models.ManyToManyField(
        User,
        through="users_tasks" ,
        through_fields=("task_id" , "user_id"),
        related_name="tasks"
    )


class users_tasks(models.Model):
    class Meta:
        db_table = "users_tasks"
    user_id = models.ForeignKey(User , name= 'user_id', on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task , name = 'task_id' , on_delete=models.CASCADE)
    
# Create your models here.
