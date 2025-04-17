from rest_framework import permissions

from .models import Workspace , Users_Workspaces

class IsOwner(permissions.BasePermission):
    message = 'Authenticated User Is Not The Workspace Owner!'

    def has_permission(self, request, view):
        workspace_id = view.kwargs.get('pk')

        return Workspace.objects.filter(
            owner=request.user,
            id=workspace_id
        ).exists()


class IsMember(permissions.BasePermission):
    message = 'Authenticated User Is Not Member In The Required Workspace!'

    def has_permission(self, request, view):
        workspace_id = view.kwargs.get('pk')
        
        workspace = Workspace.objects.filter(id=workspace_id)
        return Users_Workspaces.objects.filter(
            user=request.user,
            workspace_id=workspace_id
        ).exists()
    
class CanEdit(permissions.BasePermission):
    message = 'Authenticated User Can\'t Edit In The Required Workspace!'

    def has_permission(self, request, view):
        workspace_id = view.kwargs.get('pk')
        workspace = Workspace.objects.filter(id=workspace_id)
        membership = Users_Workspaces.objects.filter(user=request.user, workspace_id=workspace_id)
        if membership.exists():
            membership = membership.get()
            if membership.user_role != "can_view":
                return True
        return False