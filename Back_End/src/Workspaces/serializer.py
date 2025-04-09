from rest_framework import serializers

from .models import Workspace , Users_Workspaces

# from src.Users.serializer import UserSerializer
from src.Users.models import User


class UsersWorkspacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users_Workspaces
        fields = '__all__'

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