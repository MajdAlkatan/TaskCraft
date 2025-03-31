from django.db import models

from src.Tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields

from src.Users.models import User

# Create your models here.
class Workspace(TimeStampedModel):
    class Meta:
        app_label = 'Workspaces'
        db_table = 'workspaces'
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True , upload_to=f'Workspaces/{id}/') #TODO put default photo
    users = models.ManyToManyField(
        User,
        through= "Users_Workspaces",
        through_fields=("workspace_id", "user_id"),
        related_name='workspaces'
    )

    def __str__(self):
        return self.name


class Users_Workspaces(models.Model):
    class Meta:
        db_table = 'users_workspaces'
    user_id = models.ForeignKey(User , name= 'user_id', on_delete=models.CASCADE)
    workspace_id = models.ForeignKey(Workspace , name= 'workspace_id', on_delete=models.CASCADE)
    class User_Role(models.TextChoices):
        OWNER = 'owner' , 'Owner'
        PARTNER = 'partner' , 'Partner'
        CAN_EDIT = 'can_edit' , 'Can Edit'
        CAN_VIEW = 'can_view' , 'Can View'
    user_role = models.CharField(
        max_length = 8,
        choices = User_Role.choices,
        default= User_Role.CAN_VIEW
    )