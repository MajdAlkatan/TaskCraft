from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserAPI

router = DefaultRouter()
router.register(r'users' , UserAPI)

urlpatterns = [
    *router.urls
]
