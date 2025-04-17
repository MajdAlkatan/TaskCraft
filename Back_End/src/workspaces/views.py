from django.shortcuts import render 

# Create your views here.
from django.core import exceptions
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated

from users.permissions import IsClient

from .models import Workspace
from .serializers import WorkspaceSerializer
from .filters import WorkspaceFilter

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
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            self.permission_classes = [IsClient, IsAuthenticated]
        if self.action == 'owned':
            self.permission_classes.append(IsAuthenticated)
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
            if not self.request.user.is_staff:
                qs = qs.filter(owner=self.request.user)
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