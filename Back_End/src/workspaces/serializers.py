from rest_framework import serializers

from .models import Workspace , Users_Workspaces , Invite

# from src.Users.serializer import UserSerializer
from users.models import User
# from users.serializers import UserSerializer


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            'id',
            'sender',
            'receiver',
            'workspace',
            'status',
            'created_at',
            'updated_at'
        ]

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_Workspaces
        fields = [
            'id',
            'user_role'
        ]

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

        if self.context.get('add_user_field' , False):
            self.fields['user'] = serializers.PrimaryKeyRelatedField(read_only=True)
        if self.context.get('add_workspace_field' , False):
            self.fields['workspace'] = serializers.PrimaryKeyRelatedField(read_only=True)

class WorkspaceSerializer(serializers.ModelSerializer):
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
        filtered_members = []
        for member in data['members']:
            # print(f'\nmember: {member}\n')
            if member.get('user_role') != 'owner':
                filtered_members.append(member)
        data['members'] = filtered_members
        return data