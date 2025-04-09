from django.core import exceptions
from django.shortcuts import get_object_or_404

from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Workspace , User
from .serializer import WorkspaceSerializer , UsersWorkspacesSerializer

# Create your views here.

class WorkspaceAPI(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def create(self, request, *args, **kwargs):
        try:
            if not request['owner_id']:
                raise exceptions.ValidationError('owner_id may not be blank/null')
            owner = get_object_or_404(User , pk=request['owner_id'])
            serializer = UsersWorkspacesSerializer(owner)
            return super().create(request, *args, **kwargs)
        except KeyError as e:
            return Response({str(e): 'owner_id is required !'} , status=status.HTTP_400_BAD_REQUEST)
