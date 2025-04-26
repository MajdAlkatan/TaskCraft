from django.db import transaction
from rest_framework import serializers

from .models import Workspace , Users_Workspaces , Invite , Workspace_Invitation

# from src.Users.serializer import UserSerializer
from users.models import User
from tasks.serializer import WorkspaceCategoryAssignmentSerializer , WorkspaceCategoryOptionAssignmentSerializer
# from users.serializers import UserSerializer

class LocalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
            'id',
            'fullname',
            'email',
            'image',
            'created_at',
            'updated_at',
        ]

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            'id',
            'sender',
            'receiver',
            'workspace',
            'status',
            'expire_date',
            'created_at',
            'updated_at'
        ]
        extra_kwargs={
            'expire_date':{'read_only': True}
        }
    
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super().__init__(instance, data, **kwargs)
         
        if self.context.get('remove_receiver' , False):
            self.fields.pop('receiver')
        if self.context.get('remove_sender' , False):
            self.fields.pop('sender')
        if self.context.get('extend_sender' , False):
            self.fields['sender'] = LocalUserSerializer(read_only=True)

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_Workspaces
        fields = [
            'id',
            'user_role',
        ]

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super().__init__(instance, data, **kwargs)

        if self.context.get('add_user_field' , False):
            self.fields['user'] = serializers.PrimaryKeyRelatedField(read_only=True)
        if self.context.get('add_workspace_field' , False):
            self.fields['workspace'] = serializers.PrimaryKeyRelatedField(read_only=True)

class WorkspaceSerializer(serializers.ModelSerializer):
    
    owner = LocalUserSerializer(required=False)
    members = MembershipSerializer(
        many=True,
        context={
            "add_user_field": True,
            "add_workspace_field": False,
        },
        read_only=True
    )
    class Meta:
        model = Workspace
        fields = [
            'id',
            'name',
            'image',
            'owner',
            'members',
            'created_at',
            'updated_at',
        ]
        extra_kwargs={
            'image': {
                'required': False
            },
        }

    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        
        if not self.context.get('add_owner' , True):
            self.fields.pop('owner')

    def create(self, validated_data):
        # ensure user can't create more that 10 workspaces
        user_workspaces = Workspace.objects.filter(owner_id=self.context['request'].user)
        if len(user_workspaces) > 9: # there is 10 or more workspaces that this user owns
            raise serializers.ValidationError(f'User {self.context['request'].user.id} has reached the allowed limit of workspaces count !')
        
        with transaction.atomic():
            if 'image' in validated_data:
                image = validated_data.pop('image')
            instance = super().create(validated_data)
            
            if 'image' in validated_data:
                instance.image = image
                instance.save()
            
            Users_Workspaces.objects.create(
                workspace=instance,
                user=self.context['request'].user,
                user_role = 'owner'
            )
            
            #TODO: implement soft create for the main task_categories
            """
            # categories
            status_category_serializer = WorkspaceCategoryAssignmentSerializer(
                data={
                    "workspace":instance.id,
                    "name": "status"
                }
            )
            if not status_category_serializer.is_valid():
                raise serializers.ValidationError({"status_category": "can't create category [credentials not valid] [in serializer]"})
            status_category = status_category_serializer.save()

            priority_category_serializer = WorkspaceCategoryAssignmentSerializer(
                data={
                    "workspace":instance.id,
                    "name": "priority"
                }
            )
            if not priority_category_serializer.is_valid():
                raise serializers.ValidationError({"priority_category": "can't create category [credentials not valid] [in serializer]"})
            priority_category = priority_category_serializer.save()
            
            # options
            status_options_serializer = WorkspaceCategoryOptionAssignmentSerializer(
                data={
                    "workspace":instance.id,
                    "task_category":status_category.id,
                    "options":[
                        {"name":"pending"},
                        {"name":"in progress"},
                        {"name":"completed"}
                    ]
                }
            )
            if not status_options_serializer.is_valid():
                raise serializers.ValidationError({"status_options": f"can't create status options [credentials not valid] [in serializer] [{status_options_serializer.errors}]"})
            status_options_serializer.save()
            

            priority_options_serializer = WorkspaceCategoryOptionAssignmentSerializer(
                data={
                    "workspace":instance.id,
                    "task_category":priority_category.id,
                    "options":[
                        {"name":"low"},
                        {"name":"medium"},
                        {"name":"high"}
                    ]
                }
            )
            if not priority_options_serializer.is_valid():
                raise serializers.ValidationError({"priority_options": "can't create priority options [credentials not valid] [in serializer]"})
            priority_options_serializer.save()
            """

        return instance

    def update(self, instance, validated_data):
        if not Users_Workspaces.objects.filter(
            workspace=instance.id,
            user=self.context['request'].user,
            user_role='owner').exists:
            raise serializers.ValidationError('the user authenticated isn\'t the owner of the workspace')
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # print(f'\ndata[members]: {data['members']}\n')
        if not self.context.get('do_not_filter_members' , False):
            filtered_members = []
            for member in data['members']:
                # print(f'\nmember: {member}\n')
                if member.get('user_role') != 'owner':
                    filtered_members.append(member)
            data['members'] = filtered_members
        return data
    

class WorkspaceInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace_Invitation
        fields = [
            'id',
            'workspace',
            'token',
            'link',
            'expires_at',
            'valid'
        ]