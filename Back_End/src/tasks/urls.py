from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet , CategoryOptionsViewSet , TaskCategoryViewSet

router_task = DefaultRouter()
router_task.register('tasks' , TaskViewSet)

router_option = DefaultRouter()
router_option.register('category_options' , CategoryOptionsViewSet)

router_category = DefaultRouter()
router_category.register('task_categories' , TaskCategoryViewSet)


urlpatterns = [
    *router_task.urls,
    *router_category.urls,
    *router_option.urls,
]