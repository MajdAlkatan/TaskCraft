from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from .models import Task , Category_Option , Task_Category
from .serializer import TaskSerializer , TaskCreateSerializer , CategoryOptionSerializer , TaskCategoryCreateSerializer ,TaskCategorySerializer
# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TaskCreateSerializer
        return super().get_serializer_class()
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if not self.request.user.is_staff:
    #         qs = qs.filter(user = self.request.user)
    #     return qs
    

class CategoryOptionsViewSet(viewsets.ModelViewSet):
    queryset = Category_Option.objects.all()
    serializer_class = CategoryOptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user = self.request.user)
        return qs


class TaskCategoryViewSet(viewsets.ModelViewSet):
    queryset = Task_Category.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user = self.request.user)
        return qs