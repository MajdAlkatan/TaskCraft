from rest_framework import serializers

from .models import User
from workspaces.models import Workspace , Users_Workspaces
# from src.Workspaces.serializer import WorkspaceSerializer

import logging
logger = logging.getLogger(__name__)

class NestedWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name' , 'image']

class UserSerializer(serializers.ModelSerializer):
    workspaces = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'image' , 'workspaces']
        extra_kwargs = {'password': {'write_only':True}}

    def get_workspaces(self, user_obj):
        user_workspaces = Users_Workspaces.objects.filter(user=user_obj)
        workspaces_data = []
        for uw in user_workspaces:
            workspace_data = NestedWorkspaceSerializer(uw.workspace , context=self.context).data
            workspace_data['role'] = uw.user_role
            workspaces_data.append(workspaces_data)
        
        return workspaces_data



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False,
        allow_blank=False,  # Explicitly disallow empty strings
    )
    
    class Meta:
        model = User
        fields = ['fullname', 'email' , 'password']
        extra_kwargs = {
            'fullname': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        # logger.debug(f'in serializer, attrs:  {attrs}')
        try:
            if not attrs['password']:  # Check for empty string/None
                raise serializers.ValidationError({
                    'password': 'This field may not be blank (empty).'
                })
        except KeyError:
            raise serializers.ValidationError({
                'password': 'This field is required.'
            })
        
        attrs = super().validate(attrs) 

        if len(attrs['password']) < 8:
            raise serializers.ValidationError({'password': 'must be 8 characters or more'})

        return attrs
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                fullname = validated_data['fullname'],
                email = validated_data['email'],
                password = validated_data['password']
            )
            return user
        except KeyError as e:
            raise serializers.ValidationError(f'{str(e)}: this field is required !')