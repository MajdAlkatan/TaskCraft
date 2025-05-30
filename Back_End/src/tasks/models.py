from django.db import models
from users.models import User 
from workspaces.models import Workspace 
from tools.tools import TimeStampedModel
from django.utils import timezone


def user_image_upload_path(instance, filename):
    if not instance.id:
        # Handle case where instance isn't saved yet
        return f'Tasks/temp/{filename}'
    return f'Tasks/{instance.id}/{filename}'

class Task(TimeStampedModel):
    class Meta:
        app_label = "tasks"
        db_table = "tasks"
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000 , default= "There is no description")
    start_date = models.DateField(auto_now_add=False , null=True, blank=True )
    end_date = models.DateField(auto_now_add=False , null=True, blank=True )
    owner = models.ForeignKey(User , on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , default = 1)
    image = models.ImageField(null=True,blank=True , upload_to=user_image_upload_path , default="defaults/task/task.png")
    out_dated = models.BooleanField(default = False)
    users = models.ManyToManyField(
        User,
        through="users_tasks" ,
        through_fields=("task_id" , "user_id"),
        related_name="tasks"
    )

    def clean(self):
        # if self.start_date == "":
        #     self.start_date = None
        # if self.end_date == "":
        #     self.end_date = None
        
        if isinstance(self.start_date, str) and not self.start_date.strip():
            self.start_date = None
        if isinstance(self.end_date, str) and not self.end_date.strip():
            self.end_date = None
        super().clean()
    
    def is_outdated(self):
        if not self.end_date:
            return False 
        today = timezone.now().date()
        return today > self.end_date
    
    def save(self , *args , **kwargs):
        if self.end_date:
            self.out_dated = self.is_outdated()
        super().save(*args , **kwargs)

    # def valid_for_edit(self):
    #     if self.items.task_category.name == 'status':
    #         return self.items.category_option.name == "pending"
    #     return False
    


class users_tasks(models.Model):
    class Meta:
        db_table = "users_tasks"
    user = models.ForeignKey(User , name= 'user', on_delete=models.CASCADE ,)
    task = models.ForeignKey(Task , name = 'task' , on_delete=models.CASCADE , related_name = 'users_task'
                            #   related_name='owner_tasks'
                              )
    

class Task_Category(TimeStampedModel):
    class Meta:
        app_label = 'tasks'
        db_table = 'task_categories'
    name = models.CharField(max_length=20 , unique=True)
    tasks = models.ManyToManyField(
        Task,
        through="tasks_task_categories" ,
        through_fields=("task_category_id" , "task_id"),
        related_name="task_categories"
    )
    workspaces = models.ManyToManyField(
        Workspace,
        through="workspace_category_option" ,
        through_fields=("task_category_id" , "workspace_id"),
        related_name="task_categories"
    )

    def save(self , *args , **kwargs):
        self.name = self.name.lower()
        super().save(*args , **kwargs)


class Category_Option(TimeStampedModel):
    class Meta:
        app_label = 'tasks'
        db_table = 'category_options'
    name = models.CharField(max_length=20 , unique=True)
    # task_category  = models.ForeignKey(Task_Category , on_delete=models.CASCADE , related_name='options')
    tasks = models.ManyToManyField(
        Task,
        through="tasks_task_categories" ,
        through_fields=("category_option_id" , "task_id"),
        related_name="category_options"
    )
    task_categories = models.ManyToManyField(
        Task_Category,
        through="workspace_category_option" ,
        through_fields=("category_option_id" , "task_category_id"),
        related_name="category_options"
    )
    
    def save(self , *args , **kwargs):
        self.name = self.name.lower()
        super().save(*args , **kwargs)

    


class tasks_task_categories(models.Model):
    class Meta:
        db_table = "tasks_task_categories"
    task = models.ForeignKey(Task , name = 'task' , on_delete=models.CASCADE , related_name='items')
    task_category = models.ForeignKey(Task_Category , name = 'task_category' , on_delete=models.CASCADE)
    category_option = models.ForeignKey(Category_Option , name = 'category_option' , on_delete=models.CASCADE)


 


class workspace_category_option(models.Model):
    class Meta:
        db_table = "workspace_category_option"
        unique_together = [
            # ('workspace', 'task_category'),  # Workspace-Category relationship
            ('workspace', 'task_category', 'category_option')  # Workspace-Category-Option relationship
        ]
    workspace = models.ForeignKey(Workspace , on_delete = models.CASCADE)
    task_category = models.ForeignKey(Task_Category , on_delete = models.CASCADE , related_name = 'options')
    category_option = models.ForeignKey(Category_Option , on_delete = models.CASCADE , null=True,blank=True)
    
