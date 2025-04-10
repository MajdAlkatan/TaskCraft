from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import transaction

from .models import User
from workspaces.serializers import MembershipSerializer
from workspaces.models import Workspace , Users_Workspaces
# from src.Workspaces.serializer import WorkspaceSerializer

import logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(
        many=True,
        context={
            "add_user_field": False,
            "add_workspace_field": True,
        }
    )
    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'email',
            'password',
            'image',
            'memberships',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {'password': {'write_only':True}}

    def validate_password(self, value):
        if not value:  # Check for empty string/None
            raise serializers.ValidationError({'password': 'This field may not be blank (empty).'})
        if len(value) < 8:
            raise serializers.ValidationError({'password': 'must be 8 characters or more'})
        return value

    def update(self, instance, validated_data):
        user_workspaces = validated_data.pop('workspaces')
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if user_workspaces is not None:
                # validate required fields
                try:
                    if not user_workspaces['id']:
                        raise serializers.ValidationError({"id" : "this field may not be blank (empty)."})
                    if not user_workspaces['name']:
                        raise serializers.ValidationError({"name" : "this field may not be blank (empty)."})
                except KeyError as e:
                    raise serializers.ValidationError({f"{str(e)}": "this field is required!"})
                # processing the workspaces data
                for workspace in user_workspaces:
                    # check if the workspace exists
                    existed_ws = Workspace.objects.get(pk=workspace.id)
                    # if it is exist so update it
                    if existed_ws:
                        Workspace.objects.update(**workspace)
                    # if it is not exist so create the new workspace
                    else:
                        Workspace.objects.create(**workspace)
        return instance





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'})
    

    class Meta:
        model = User
        fields = ['fullname', 'email' , 'password']
        extra_kwargs = {
            'fullname': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
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
            with transaction.atomic():
                user = User.objects.create_user(
                    fullname = validated_data['fullname'],
                    email = validated_data['email'],
                    password = validated_data['password']
                )

                default_workspace = Workspace.objects.create(
                    name="Default Workspace",
                    image=None, #TODO put a default workspace-image path
                    owner=user
                )

            return user
        except KeyError as e:
            raise serializers.ValidationError(f'{str(e)}: this field is required !')
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Use email instead of username

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super().validate(attrs)
        # Add custom claims or user data if needed
        data['user'] = {
            'email': self.user.email,
            'fullname': self.user.fullname
        }
        return data