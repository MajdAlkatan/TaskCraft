from django.db import models
from django.db.models import Q
from django.core.signing import TimestampSigner
from django.conf import settings
from datetime import datetime , timedelta

import uuid
# Create your models here.

from tools.tools import TimeStampedModel #auto insert the created_at & updated_at fields
from users.models import User
from .utils.crypto import Crypto

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
    code = models.UUIDField(default=uuid.uuid4 , unique=True , editable=False)

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

    def save(self,*args,**kwargs):
        if (self.user_role != 'owner' and self.user_role != 'can_edit' and self.user_role != 'can_view'):
            print(f'\n\nuser role can\'t be {self.user_role}\n\n')
            return False
        super().save(*args,**kwargs)
        return True



def default_invite_expire_date():
    return datetime.today() + timedelta(days=7)
class Invite(TimeStampedModel):
    class Meta:
        db_table = 'invites'
        """
        constraints=[
            models.UniqueConstraint(
                fields=['sender' , 'receiver' , 'workspace'],
                condition = Q(status='pending'),
                name='unique_pending_invite'
            ),
        ]
        """
    sender = models.ForeignKey(User , related_name='sent_invites' , on_delete=models.CASCADE)
    receiver = models.ForeignKey(User , related_name='received_invites' , on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace , related_name='invites' , on_delete=models.CASCADE)
    class Status_Choices(models.TextChoices):
        PENDING = 'pending',
        ACCEPTED = 'accepted',
        REJECTED = 'rejected'
    status = models.CharField(
        max_length=8,
        choices=Status_Choices,
        default=Status_Choices.PENDING
    )
    expire_date = models.DateField(default=default_invite_expire_date, editable=False)

    def save(self,*args,**kwargs):
        
        if (self.status != 'pending' and self.status != 'accepted' and self.status != 'rejected'):
            print(f'\n\nINVITE STATUS can\'t be {self.status}\n\n')
            return False
        
        #instead of the unique constraint for status='pending'
        if Invite.objects.filter(
            sender=kwargs['sender'],
            receiver=kwargs['receiver'],
            workspace=kwargs['workspace'],
            status='pending'
        ).exists:
            print(f'\n\nTHIS INVITE ALREADY EXISTS!\n\n')
            raise Exception("THIS INVITE ALREADY EXISTS!")


        super().save(*args,**kwargs)
        return True

    # checking if the invite still waiting for an action from user
    def valid_invite(self):
        if self.status == 'pending':
            return True
        return False

    def __str__(self):
        return f"user {self.sender.fullname} sent an invite to user {self.receiver.fullname} into the workspace {self.workspace.name}"
    

def workspace_invitation_expiring_date_time():
    return datetime.now() + timedelta(hours=24)
class Workspace_Invitation(TimeStampedModel):
    class Meta:
        db_table='workspace_invitations'
    
    workspace = models.ForeignKey(Workspace , on_delete=models.CASCADE , related_name='invitation_links')
    token = models.CharField(max_length=255, unique=True , editable=False)
    link = models.CharField(max_length=255 , unique=True)
    expires_at = models.DateTimeField(editable=False)
    valid = models.BooleanField(default=False)


    def save(self, *args , **kwargs):
        if not self.id:
            #instead of the unique constraint for valid=True
            if Workspace_Invitation.objects.filter(
                workspace = kwargs['workspace'],
                valid=True
            ).exists():
                print(f'\n\nTHIS WORKSPACE ALREADY HAVE AN INVITATION LINK!\n\n')
                raise Exception("THIS WORKSPACE ALREADY HAVE AN INVITATION LINK!")
        
            self.token = self.create_invitation_token()
            # Encrypt token before creating the link and put the encrypted one in the link
            crypto = Crypto()
            encrypted_token = crypto.encrypt(str(self.token))
            self.link = f'{settings.BASE_URL}/invite-link/{encrypted_token}/lets-join/'
            self.expires_at = workspace_invitation_expiring_date_time()
        return super().save(*args , **kwargs)


    def create_invitation_token(self):
        workspace = Workspace.objects.filter(id = self.workspace).first()
        signer = TimestampSigner()
        return signer.sign(str(workspace.code))


    def did_expired(self):
        return (self.expires_at > datetime.now())

    def __str__(self):
        return f'invitation-link [{self.link}] for workspace [{self.workspace}] by token [{self.token}], expires_at [{self.expires_at}]'