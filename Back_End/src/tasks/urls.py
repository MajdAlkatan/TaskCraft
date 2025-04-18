from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet , CategoryOptionsViewSet , TaskCategoryViewSet 

router_task = DefaultRouter()
router_task.register(r'tasks' , TaskViewSet)

router_option = DefaultRouter()
router_option.register(r'category_options' , CategoryOptionsViewSet)

router_category = DefaultRouter()
router_category.register(r'task_categories' , TaskCategoryViewSet)


urlpatterns = [
    *router_task.urls,
    *router_category.urls,
    *router_option.urls,
    # path('task_categories/assign/' , AssignOptionsToCategoryAPIView.as_view() ), 
]