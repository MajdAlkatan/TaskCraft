from rest_framework import serializers

from .models import Workspace , Users_Workspaces

# from src.Users.serializer import UserSerializer
from users.models import User


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
        


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'fullname' , 'email' , 'image']

class WorkspaceSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'users']
    
    def get_users(self, workspace_obj):
        workspace_users = Users_Workspaces.objects.filter(workspace=workspace_obj)
        users_data = []
        for wu in workspace_users:
            user_data = NestedUserSerializer(wu.user , context=self.context).data
            user_data['role'] = wu.user_role
            users_data.append(user_data)
        
        return users_data