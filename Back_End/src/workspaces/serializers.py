from rest_framework import serializers

from .models import Workspace , Users_Workspaces , Invite

# from src.Users.serializer import UserSerializer
from users.models import User


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
            self.fields['user'] = serializers.PrimaryKeyRelatedField()
        if self.context.get('add_workspace_field' , False):
            self.fields['workspace'] = serializers.PrimaryKeyRelatedField()

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    members = MembershipSerializer(
        many=True,
        context={
            "add_user_field": True,
            "add_workspace_field": False,
        }
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
            'updated_at,'
        ]