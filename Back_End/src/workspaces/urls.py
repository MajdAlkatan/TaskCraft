from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WorkspaceViewSet , CreateWorkspaceInvitationLink , GetWorkspaceInvitationLink , JoinWorkspaceViaInvitationLink

router = DefaultRouter()
router.register(r'workspaces' , WorkspaceViewSet)

urlpatterns = [
    *router.urls,
    path('create-invite-link/<int:workspace_id>/' , CreateWorkspaceInvitationLink.as_view()),
    path('get-invite-link/<int:workspace_id>/' , GetWorkspaceInvitationLink.as_view()),
    path('invite-link/<str:invitation_token>/' , JoinWorkspaceViaInvitationLink.as_view())
]
