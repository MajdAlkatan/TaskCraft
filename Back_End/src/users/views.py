from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from dateutil.parser import parse
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView

from workspaces.models import Invite , Users_Workspaces
from workspaces.serializers import InviteSerializer

from .models import User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    ChangeImageSerializer,
)
from .filters import UserFilter
# from .permissions import IsClient

# import pdb;
# Create your views here.

import logging
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
    filterset_class = UserFilter
    search_fields = ['fullname', 'email']
    ordering_fields = ['fullname', 'email', 'created_at', 'updated_at']
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        
        if (self.action == 'create' or self.action == 'destroy'
            or self.action == 'update' or self.action == 'partial_update'
            or self.action == 'received_invites' or self.action == 'sent_invites'
            or self.action == 'cancel_invite' or self.action == 'reject_invite' or self.action == 'accept_invite'):
            self.permission_classes.append(IsAuthenticated)

        if self.action == 'list':
            if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
                if not self.request.user.is_staff:
                    self.permission_classes.append(IsAuthenticated)
       
        if self.action == 'retrieve':
            if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
                if not self.request.user.is_staff:
                    self.permission_classes.append(IsAdminUser)
        return super().get_permissions()
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
            if not self.request.user.is_staff:
                qs = qs.filter(fullname=self.request.user.fullname)
                # normal user can view and update only his own info
        
        return qs

    @action(detail=False , methods=['patch'] , serializer_class=ChangeImageSerializer)
    def change_image(self , request):
        serializer = self.get_serializer(request.user , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    # Here We put 'detail-False' because even admin shouldn't be able to change users passwords for security reasons
    @action(detail=False , methods=['patch'] , serializer_class=ChangePasswordSerializer)
    def change_password(self , request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"new_password": serializer.validated_data['new_password']} , status=status.HTTP_202_ACCEPTED)


    def partial_update(self, request, *args, **kwargs): # this is updating user fullname only
        if 'workspaces' in request.data:
            request.data.pop('workspaces')
        if 'image' in request.data:
            request.data.pop('image')
        if 'password' in request.data:
            request.data.pop('password')
        return super().partial_update(request, *args, **kwargs)

    # register
    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    @action(detail=False, methods=['post'] , serializer_class=RegisterSerializer)
    def register(self, request):
        # logger.debug(f"Raw request data: {request.data}")
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
    # ------------------------ Invites section ------------------------ #

    @action(detail=False , methods=['get'] , serializer_class=InviteSerializer)
    def received_invites(self , request):
        invites = Invite.objects.filter(receiver=request.user , status='pending').all()
        serializer = self.get_serializer(
            instance=invites,
            many=True,
            context={
                'remove_receiver': True,
                'extend_sender': True
            }
        )


        # filtering the data to exclude the expired invites and delete them
        filtered_data = []
        for invite_item in serializer.data:
            if (parse(invite_item["expire_date"]) < datetime.today()):
                invite = Invite.objects.get(id=invite_item['id'])
                invite.delete()
            else:
                filtered_data.append(invite_item)
        
        
        return Response(
            {
                "receiver_id":request.user.id,
                "invites":filtered_data
            },
            status.HTTP_200_OK
        )

    @action(detail=False , methods=['get'] , serializer_class=InviteSerializer)
    def sent_invites(self , request):
        invites = Invite.objects.filter(sender=request.user , status='pending').all()
        serializer = self.get_serializer(
            instance=invites,
            many=True,
            context={
                'remove_sender': True,
            }
        )


        # filtering the data to exclude the expired invites and delete them
        filtered_data = []
        for invite_item in serializer.data:
            if (parse(invite_item["expire_date"]) < datetime.today()):
                invite = Invite.objects.get(id=invite_item['id'])
                invite.delete()
            else:
                filtered_data.append(invite_item)
        
        
        return Response(
            {
                "sender_id":request.user.id,
                "invites":filtered_data
            },
            status.HTTP_200_OK
        )

    @action(detail=False , methods=['post','patch'] , serializer_class=InviteSerializer)
    def accept_invite(self , request):
        if not request.data.get('invite_id'):
            return Response({"message": "the invite_id is required!"}, status.HTTP_400_BAD_REQUEST)
        invite = Invite.objects.filter(id=request.data.get('invite_id')).first()
        if not invite:
            return Response({"message": "the invite specified doesn't exist!"}, status.HTTP_400_BAD_REQUEST)
        if not invite.receiver == request.user:
            return Response({"message": "the invite specified doesn't belong to the authenticated user!"}, status.HTTP_400_BAD_REQUEST)
        if not invite.valid_invite():
            return Response({"message": "the invite specified status isn't pending! it can't be updated"}, status.HTTP_400_BAD_REQUEST)
        
        if not (invite.expire_date < datetime.today()):
            invite.delete()
            return Response({"invite": "the specified invite is expired!"}, status.HTTP_400_BAD_REQUEST)
        
        invite.status = 'accepted'
        invite.save()

        Users_Workspaces.objects.create(
            user=request.user,
            workspace=invite.workspace,
            user_role='can_view'
        )

        serializer = self.get_serializer(invite)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @action(detail=False , methods=['patch'] , serializer_class=InviteSerializer)
    def reject_invite(self , request):
        if not request.data.get('invite_id'):
            return Response({"message": "the invite_id is required!"}, status.HTTP_400_BAD_REQUEST)
        invite = Invite.objects.filter(id=request.data.get('invite_id')).first()
        if not invite:
            return Response({"message": "the invite specified doesn't exist!"}, status.HTTP_400_BAD_REQUEST)
        if not invite.receiver == request.user:
            return Response({"message": "the invite specified doesn't belong to the authenticated user!"}, status.HTTP_400_BAD_REQUEST)
        if not invite.valid_invite():
            return Response({"message": "the invite specified status isn't pending! it can't be updated"}, status.HTTP_400_BAD_REQUEST)
        
        if not (invite.expire_date < datetime.today()):
            invite.delete()
            return Response({"invite": "the specified invite is expired!"}, status.HTTP_400_BAD_REQUEST)
        
        invite.delete()
        return Response(None, status.HTTP_202_ACCEPTED)

    @action(detail=False , methods=['delete'] , serializer_class=InviteSerializer)
    def cancel_invite(self , request):
        try:
            if not request.data.get('invite_id'):
                return Response({"message": "the invite_id is required!"}, status.HTTP_400_BAD_REQUEST)
            invite = Invite.objects.filter(id=request.data['invite_id']).first()
            if not invite:
                return Response({"message": "the invite specified doesn't exist!"}, status.HTTP_400_BAD_REQUEST)
            if not invite.sender == request.user:
                return Response({"message": "the invite specified doesn't belong to the authenticated user!"}, status.HTTP_400_BAD_REQUEST)
            if not invite.valid_invite():
                return Response({"message": "the invite specified status isn't pending! it can't be canceled/deleted"}, status.HTTP_400_BAD_REQUEST)
            invite.delete()
            return Response(None, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"Error in cancel_invite: {str(e)}")
            return Response(
                {"message": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    