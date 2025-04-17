from rest_framework import permissions

from .models import Workspace , Users_Workspaces

class IsOwner(permissions.BasePermission):
    message = 'Authenticated User Is Not The Workspace Owner!'

    def has_permission(self, request, view):
        if Workspace.objects.filter(owner=request.user, id=view.pk).exists():
            return True
        return False


class IsMember(permissions.BasePermission):
    message = 'Authenticated User Is Not Member In The Required Workspace!'

    def has_permission(self, request, view):
        workspace = Workspace.objects.filter(id=view.pk)
        if Users_Workspaces.objects.filter(user=request.user, workspace=workspace).exists():
            return True
        return False
    
class CanEdit(permissions.BasePermission):
    message = 'Authenticated User Can\'t Edit In The Required Workspace!'

    def has_permission(self, request, view):
        workspace = Workspace.objects.filter(id=view.pk)
        membership = Users_Workspaces.objects.filter(user=request.user, workspace=workspace)
        if membership.exists():
            membership = membership.get()
            if membership.user_role != "can_view":
                return True
        return False