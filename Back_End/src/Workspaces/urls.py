from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WorkspaceAPI

router = DefaultRouter()
router.register(r'workspaces' , WorkspaceAPI)

urlpatterns = [
    *router.urls
]


