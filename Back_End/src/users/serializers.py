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
        },
        required=False
    )
    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'email',
            'image',
            'memberships',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'image': {
                'required': False
            },
            'email': {
                'read_only': True # user can't change the email specified
            },
            'fullname': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

class ChangeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image']
        extra_kwargs = {
            'image': {
                'required': True
            }
        }

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True , write_only=True)
    new_password = serializers.CharField(required=True , write_only=True)

    def validate_old_password(self , value):
        if not value:
            raise serializers.ValidationError({'old_password': 'This field may not be blank (empty).'})
        from django.contrib.auth.hashers import check_password
        if not check_password(value , self.context['request'].user.password):
            raise serializers.ValidationError({"old_password": "doesn't match the password"})
        return value
    def validate_new_password(self, value):
        if not value:
            raise serializers.ValidationError({'new_password': 'This field may not be blank (empty).'})
        if len(value) < 8:
            raise serializers.ValidationError({'new_password': 'must be 8 characters or more'})
        return value

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

                Users_Workspaces.objects.create(
                    user=user,
                    workspace=default_workspace,
                    user_role='owner'
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