from django.shortcuts import render
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User
from .serializers import UserSerializer , RegisterSerializer
# Create your views here.

import logging
logger = logging.getLogger(__name__)


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
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