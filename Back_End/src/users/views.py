from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer , RegisterSerializer , ChangePasswordSerializer
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

    @action(detail=True , methods=['patch'])
    def change_image(self , request):
        pass #TODO

    # Here We put 'detail-False' because even admin shouldn't be able to change users passwords for security reasons
    @action(detail=False , methods=['patch'] , serializer_class=ChangePasswordSerializer)
    def change_password(self , request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"new_password": serializer.validated_data['new_password']} , status=status.HTTP_202_ACCEPTED)


    def partial_update(self, request, *args, **kwargs): # canceled because the PUT request actually updates only the fullname
        return Response(
            {"detail": "Method not allowed"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    # update-user-profile-info (PUT) (with the current user-model the PUT request is changing the fullname only)
    def update(self, request, *args, **kwargs):
        # PUT request shouldn't include password or image update
        # there is an independent api's for each of these fields
        if 'password' in request.data:
            request.data.pop('password')
        if 'image' in request.data:
            request.data.pop('image')
        if 'memberships' in request.data:
            request.data.pop('memberships')
        return super().update(request, *args, **kwargs)

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