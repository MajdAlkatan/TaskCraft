from rest_framework import permissions

from django.contrib.auth.hashers import check_password

from .models import Client


class IsClient(permissions.BasePermission):
    message = "you are not one of our clients idiot !"


    def has_permission(self, request, view):
        if not 'HTTP_CLIENT_SECRET' in request.META or not 'HTTP_CLIENT_USERNAME' in request.META:
            return False
        
        # print('\n\narrived to permission code\n\n')

        client = Client.objects.filter(username=request.META['HTTP_CLIENT_USERNAME'])
        
        # print(f'\nusername: {request.META['HTTP_CLIENT_USERNAME']}\n')
        # print('\nHere 1\n')

        if not client.exists():
            return False
        
        # print('\nHere 2\n')
        
        client = client.get()

        # print('\nHere 2.5\n')

        if not check_password(request.META['HTTP_CLIENT_SECRET'] , client.secret):
            return False
        
        # print('\nHere 3\n')

        return True