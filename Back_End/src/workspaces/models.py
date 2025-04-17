from django.db import models

# Create your models here.
from django.db import models

from tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields
from users.models import User

# Create your models here.
def workspace_image_upload_path(instance , filename):
    if not instance.id:
        # Handle case where instance isn't saved yet
        return f'Workspaces/temp/{filename}'
    return f'Workspaces/{instance.id}/{filename}'
class Workspace(TimeStampedModel):
    class Meta:
        db_table = 'workspaces'
    name = models.CharField(max_length=255)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=workspace_image_upload_path
    ) #TODO put default photo
    owner = models.ForeignKey(User , related_name='own_workspaces' , on_delete=models.CASCADE, null=False, blank=False)
    users = models.ManyToManyField(
        User,
        through= "Users_Workspaces",
        through_fields=("workspace", "user"),
        related_name='workspaces'
    )

    def __str__(self):
        return self.name


class Users_Workspaces(models.Model):
    class Meta:
        db_table = 'users_workspaces'
        unique_together= ['user' , 'workspace']
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='memberships')
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , related_name='members')
    class User_Role(models.TextChoices):
        OWNER = 'owner'
        CAN_EDIT = 'can_edit'
        CAN_VIEW = 'can_view'
    user_role = models.CharField(
        max_length = 8,
        choices = User_Role.choices,
        default= User_Role.CAN_VIEW
    )

class Invite(TimeStampedModel):
    class Meta:
        db_table = 'invites'
        unique_together = ['sender' , 'receiver' , 'workspace']
    sender = models.ForeignKey(User , related_name='sent_invites' , on_delete=models.CASCADE)
    receiver = models.ForeignKey(User , related_name='received_invites' , on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace , related_name='invites' , on_delete=models.CASCADE)
    class Status_Choices(models.TextChoices):
        PENDING = 'pending' , 'Pending',
        ACCEPTED = 'accepted' , 'Accepted',
        REJECTED = 'rejected' , 'Rejected',
        CANCELED = 'canceled' , 'Canceled'
    status = models.CharField(
        max_length=8,
        choices=Status_Choices,
        default=Status_Choices.PENDING
    )

    # checking if the invite still waiting for an action from user
    def invalid_invite(self):
        if self.status == 'pending':
            return False
        return True

    def __str__(self):
        return f"user {self.sender.fullname} sent an invite to user {self.receiver.fullname} into the workspace {self.workspace.name}"