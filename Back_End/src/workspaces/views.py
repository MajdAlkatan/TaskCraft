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

from .models import Workspace
from .serializers import WorkspaceSerializer
from .filters import WorkspaceFilter

# Create your views here.

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
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

    def get_queryset(self):
        qs = super().get_queryset()
        if 'HTTP_AUTHORIZATION' in self.request.META: # if there is an authentication header
            if not self.request.user.is_staff:
                qs = qs.filter(fullname=self.request.user.fullname)
                # normal user can view and update only his own info
        return qs

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        return Response(
            'method not allowed',
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        # return super().create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        return Response(
            'method not allowed',
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        # return super().update(request, *args, **kwargs)
    def partial_update(self, request, *args, **kwargs):
        return Response(
            'method not allowed',
            status.HTTP_405_METHOD_NOT_ALLOWED
        )
        # return super().partial_update(request, *args, **kwargs)
