from django.shortcuts import render
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer , RegisterSerializer , CustomTokenObtainPairSerializer
# Create your views here.

import logging
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action == 'retrieve':
            self.permission_classes = [IsAdminUser]
            # this means only admin can retrieve specific user info,
            # while normal user can access his own info by /users/ (list){because it will list just his own profile}
        return super().get_permissions()
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(fullname=self.request.user.fullname)
            # normal user can view and update only his own info
        return qs

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