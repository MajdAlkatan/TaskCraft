from django.shortcuts import render 

# Create your views here.
from django.core import exceptions
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.signing import TimestampSigner , SignatureExpired , BadSignature

from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets , status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated

# from users.permissions import IsClient

from .permissions import IsMember , IsOwner
from .models import Workspace , Users_Workspaces , Invite , Workspace_Invitation
from .serializers import WorkspaceSerializer , InviteSerializer , MembershipSerializer , WorkspaceInvitationSerializer
from .filters import WorkspaceFilter
from .utils.crypto import Crypto

# Create your views here.

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    # Pagination
    pagination_class = PageNumberPagination
    pagination_class.page_size=50
    pagination_class.max_page_size=120
    pagination_class.page_size_query_param='size'
    # filtering/searching/ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = WorkspaceFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' or self.action == 'owned':
            self.permission_classes.append(IsAuthenticated)
        if self.action == 'list':
            if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
                if not self.request.user.is_staff:
                    self.permission_classes.append(IsAuthenticated)
        if self.action == 'retrieve':
            if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
                if not self.request.user.is_staff:
                    self.permission_classes.append(IsAdminUser)
        if self.action == 'members' or self.action == 'leave':
            self.permission_classes.append(IsAuthenticated)
            self.permission_classes.append(IsMember)
        if self.action == 'invite_user' or self.action == 'kick_user' or self.action == 'change_user_role':
            self.permission_classes.append(IsAuthenticated)
            self.permission_classes.append(IsOwner)
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
                if not self.request.user.is_staff:
                    qs = Workspace.objects.filter(
                        Q(members__user=self.request.user)|
                        Q(owner=self.request.user)
                    )
                    # normal user can view and update only his own info
        if self.action == 'owned':
            qs = qs.filter(owner=self.request.user)
        return qs


    # Read
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    # Create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    # Update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    def partial_update(self, request, *args, **kwargs):
        """
        request:
            {
                "name": "new workspace name",
                "image": file[workspace-image.jpg]
            }
        """
        return super().partial_update(request, *args, **kwargs)
    
    # Delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # Get-User-Workspaces
    @action(detail=False , methods=['get'])
    def owned(self , request):
        serializer = self.get_serializer(
            self.get_queryset(),
            many=True,
            context={
                'add_owner': False
            }
        )
        return Response(
            data={
                "user_id": self.request.user.id,
                "email": self.request.user.email,
                "fullname": self.request.user.fullname,
                "workspaces": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True , methods=['get'])
    def members(self , request , pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(
            instance=workspace,
            context={
                'add_owner': False,
                'do_not_filter_members': True
            }
        )
        return Response(serializer.data.get('members') , status=status.HTTP_200_OK)
    
    @action(detail=True , methods=['get'])
    def owner(self , request , pk=None):
        workspace = self.get_object()
        serializer = self.get_serializer(instance=workspace)
        return Response(serializer.data.get('owner') , status=status.HTTP_200_OK)
    
    @action(detail=True , methods=['delete'])
    def leave(self , request , pk):
        workspace = self.get_object()
        if workspace.owner == request.user:
            return Response({"message" : "user that wants to leave workspace is the owner !"} , status.HTTP_400_BAD_REQUEST)
        membership = Users_Workspaces.objects.filter(user=request.user,workspace=workspace)
        if not membership.exists():
            return Response({"message" : "user that wants to leave workspace is already not member !"} , status.HTTP_400_BAD_REQUEST)
        membership = membership.get()
        membership.delete()
        #TODO: Must delete all tasks he created or he was contributing in. @Ali_Almusfi
        return Response(None , status.HTTP_204_NO_CONTENT)


    # Invites

    @action(detail=True , methods=['post'] , serializer_class=InviteSerializer)
    def invite_user(self, request , pk):
        if request.data.get('receiver') == request.user.id:
            return Response({"message": "User can not invite himself :) "} , status.HTTP_400_BAD_REQUEST)
        # checking if the user already a member in the workspace
        workspace = self.get_object()
        membership = Users_Workspaces.objects.filter(user_id=request.data.get('receiver') , workspace=workspace)
        if membership.exists():
            return Response({"message": "Invitee user in already a member in the workspace specified"} , status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(
            data={
                "workspace":pk,
                "sender":request.user.id,
                **request.data
            }
        )

        if serializer.is_valid():
            serializer.save(status='pending')
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True , methods=['delete'])
    def kick_user(self, request , pk):
        workspace = self.get_object()
        if not (workspace.owner == request.user):
            return Response({"message" : "user that wants to kick users is not the owner !"} , status.HTTP_400_BAD_REQUEST)
        membership = Users_Workspaces.objects.filter(user=request.data.get('kicked_user'),workspace=workspace)
        if not membership.exists():
            return Response({"message" : "user that you want to kick from workspace is already not a member in the specified workspace !"} , status.HTTP_400_BAD_REQUEST)
        membership = membership.get()
        membership.delete()
        #TODO: Must delete all tasks he created or he was contributing in. @Ali_Almusfi
        return Response(None , status.HTTP_204_NO_CONTENT)
    
    # User_Role
    @action(detail=True , methods=['patch'] , serializer_class=MembershipSerializer)
    def change_user_role(self , request , pk):
        workspace = self.get_object()
        if 'workspace' in request.data:
            request.data.pop('workspace') # workspace mustn't be passed to the serializer from request!
        if not 'user' in request.data:
            return Response({'user': "user field is required!"} , status.HTTP_400_BAD_REQUEST)
        if not 'user_role' in request.data:
            return Response({'user_role': "user_role field is required!"} , status.HTTP_400_BAD_REQUEST)
        if request.data.get('user_role') == 'owner':
            return Response({'user_role': "user_role field can't be 'owner'!"} , status.HTTP_400_BAD_REQUEST)

        #TODO validate other data exists in request.data
        
        membership = Users_Workspaces.objects.filter(workspace=workspace , user=request.data.get('user'))
        if not membership.exists(): # "user" must be a member in the workspace
            return Response({'user': "user specified is not a member in the specified workspace!"} , status.HTTP_400_BAD_REQUEST)
        membership = membership.get()
        if membership.user_role == 'owner': # user_role can't be "owner" & owner can't be changed into can_edit or can_view !
            return Response({'user': "user specified is the owner of the specified workspace!"}, status.HTTP_400_BAD_REQUEST)
        if membership.user_role == request.data.get('user_role'): # "user_role" can't be the same as the "user" old role ! (performance)
            return Response({'user_role': "user_role specified is the same as the old user_role! you are changing nothing"}, status.HTTP_400_BAD_REQUEST)
        membership.user_role = request.data.get('user_role')
        if not membership.save():
            return Response({'message': "membership in not saved because user_role you want is not valid!"}, status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(
            membership,
            context={
                'add_workspace_field':True,
                'add_user_field':True,
            }
        )
        return Response(serializer.data , status.HTTP_202_ACCEPTED)
        
        """
        serializer = self.get_serializer(
            context={
                'add_workspace_field':True,
                'add_user_field':True,
            },
            **request.data,
            workspace=workspace,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_202_ACCEPTED)
        return  Response(serializer.errors , status.HTTP_400_BAD_REQUEST)
        """

        """
        PATCH: http://127.0.0.1/api/workspaces/{id}/change_user_role/
            body:
                {
                    "user": 1,
                    "user_role": "can_edit"
                }
            instructions:
            1. owner can't be changed into can_edit or can_view [Done]
            2. user_role can't be "owner" [Done]
            3. "user" must be a member in the workspace [Done]
            4. "user_role" can't be the same as the "user" old role ! (performance) [Done]
        """


# Workspace-Invitations

def is_invitation_valid(expires_at , token):
    if (expires_at < timezone.now()):
        print(f'\n\n\nexpires_at > timezone.now()\n\n\n')
        return False
    signer = TimestampSigner()
    try:
        original = signer.unsign(token , max_age=(60*60*24))
        return True
    except SignatureExpired:
        print(f'\n\n\nSignatureExpired\n\n\n')
        return False
    except BadSignature:
        print(f'\n\n\nBadSignature\n\n\n')
        return False


class CreateWorkspaceInvitationLink(APIView):
    permission_classes = [IsAuthenticated, IsMember]
    def post(self, request, workspace_id):
        # make sure workspace exists
        workspace = Workspace.objects.filter(id=workspace_id)
        if not workspace.exists():
            return Response({"workspace_id": "workspace specified is not exists!"} , status.HTTP_404_NOT_FOUND)
        # get the workspace
        workspace = workspace.get()
        
        # check if there is already a valid invitation for the specified workspace
        old_invitation = Workspace_Invitation.objects.filter(workspace=workspace , valid=True)
        if old_invitation.exists():
            old_invitation = old_invitation.get()
            if is_invitation_valid(old_invitation.expires_at , old_invitation.token):
                return Response({"message": "there is already a valid invitation for this workspace! (use the Get-Workspace-Invitation-Link)"} , status.HTTP_400_BAD_REQUEST)
            else:
                old_invitation.valid = False
                old_invitation.save()
        
        # create invitation
        invitation = Workspace_Invitation.objects.create(workspace=workspace)

        return Response({"link":invitation.link} , status.HTTP_201_CREATED)
    
class GetWorkspaceInvitationLink(APIView):
    permission_classes = [IsAuthenticated , IsMember]
    def get(self , request ,workspace_id):
        # make sure workspace exists
        workspace = Workspace.objects.filter(id=workspace_id)
        if not workspace.exists():
            return Response({"workspace_id": "workspace specified is not exists!"} , status.HTTP_404_NOT_FOUND)
        # get the workspace
        workspace = workspace.get()

        # check if there is already a valid invitation for the specified workspace
        invitation = Workspace_Invitation.objects.filter(workspace=workspace , valid=True)
        if not invitation.exists():
            return Response({"invitation": "there is no invitation for this workspace or the old one has been expired! Please create a new invitation link using the create-invitation-link endpoint"} , status.HTTP_404_NOT_FOUND)
        # getting invitation
        invitation = invitation.get()

        if not is_invitation_valid(invitation.expires_at , invitation.token):
            invitation.valid = False
            invitation.save() #TODO: make sure this is working
            return Response({"invitation": "invitation has been expired! Please create a new invitation link using the create-invitation-link endpoint"} , status.HTTP_400_BAD_REQUEST)
        
        return Response({"link": invitation.link} , status.HTTP_200_OK)
        

class JoinWorkspaceViaInvitationLink(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request , invitation_token):

        # Decrypting token
        crypto = Crypto()
        try:
            token = crypto.decrypt(invitation_token)
        except Exception as e:
            return Response({"message": "Decryption failed"}, status.HTTP_400_BAD_REQUEST)
        
        
        # check if the token correct and the invitation exists
        invitation = Workspace_Invitation.objects.filter(token=token)
        if not invitation.exists():
            return Response({"invitation_token": "there is no invitation for this workspace!"} , status.HTTP_404_NOT_FOUND)
        # getting invitation
        invitation = invitation.get()

        if not is_invitation_valid(invitation.expires_at , invitation.token):
            invitation.valid = False
            invitation.save() #TODO: make sure this is working
            return Response({"invitation": "invitation has been expired! Please create a new invitation link using the create-invitation-link endpoint"} , status.HTTP_400_BAD_REQUEST)

        membership = Users_Workspaces.objects.create(
            workspace=invitation.workspace,
            user=request.user,
            user_role= 'can_view'
        )

        serializer = self.get_serializer(
            membership,
            context={
                'add_workspace_field':True,
                'add_user_field':True,
            }
        )
        return Response(serializer.data , status.HTTP_201_CREATED)

        

