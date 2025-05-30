from django.shortcuts import render
from rest_framework import viewsets , status , filters , generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from .models import Task , Category_Option , Task_Category , workspace_category_option ,users_tasks
from .serializer import TaskSerializer , TaskCreateSerializer , CategoryOptionSerializer  ,TaskCategorySerializer , ChangeImageSerializer , WorkspaceCategoryAssignmentSerializer , WorkspaceCategoryOptionAssignmentSerializer , UpdateCategoryOptionSerializer , UpdateTaskCategorySerializer
from .filter import TaskFilter
from workspaces.models import Users_Workspaces
from workspaces.permissions import IsOwner , IsMember , CanEdit
# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
        # IsCliet, TODO
    ]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size=5
    pagination_class.max_page_size=10
    pagination_class.page_size_query_param='size'


    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    search_fields = ['title' , 'description']
    ordering_fields = ['title']


    def update_outdated_status(self, task):
        if task.end_date:
            new_status = task.is_outdated()
            if task.out_dated != new_status:
                task.out_dated = new_status
                task.save(update_fields=['out_dated'])
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_outdated_status(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        for task in queryset:
            self.update_outdated_status(task)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action == 'create' or self.action == 'update' or self.action == 'destroy':
            self.permission_classes.append(IsAuthenticated , CanEdit)
        elif self.action == 'list' or self.action == 'retrieve':
            self.permission_classes.append(IsAuthenticated , IsMember)

        

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return TaskCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()

        # workspace_id = self.request.data.get('workspace')

        # if workspace_id:
        #     qs = qs.filter(workspace_id=workspace_id)

        # if 'HTTP_AUTHORIZATION' in self.request.META:
        #     if not self.request.user.is_staff:
        #         qs = qs.filter(
        #             workspace=self.request.user,
        #             # owner=self.request.user
        #         )
                # qs = qs.filter(owner = self.request.user.workspace)
                # 
                # qs = qs.filter(user = self.request.user)
        # self.
        # workspace_id = Users_Workspaces.objects.filter(user = self.request.user).values_list('workspace', flat=True).first()
        # qs = qs.filter(workspace = workspace_id)
        return qs
    
    @action(detail = True , methods = ['patch'] , serializer_class = ChangeImageSerializer )
    def change_image(self , request , pk=None):
        try:
            task = self.get_object()
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO
        # if task.owner != request.user:  
        #     return Response({'error': 'You are not the owner of this task'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        
        
    

class CategoryOptionsViewSet(viewsets.ModelViewSet):
    queryset = Category_Option.objects.all()
    serializer_class = CategoryOptionSerializer
    permission_classes = [
        IsAuthenticated,
        # IsCliet, TODO
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        # if 'HTTP_AUTHORIZATION' in self.request.META:
        #     if not self.request.user.is_staff:
        #         # Filter by workspace - adjust field names based on your actual model
        #         user_workspace = self.request.user.workspace
        #         qs = qs.filter(workspace=user_workspace)
        workspace_id = Users_Workspaces.objects.filter(user = self.request.user).first()
        category_option_id = workspace_category_option.objects.filter(workspace = workspace_id.workspace).values_list('category_option', flat=True)
        qs = qs.filter(id__in = category_option_id)
        return qs
    
    def destroy(self, request, *args, **kwargs ):
        workspace_id = request.data.get('workspace')
        task_category_id = request.data.get('task_category')
        category_option_id = request.data.get('category_option')
        if not workspace_id or not task_category_id or not category_option_id:
            return Response(
                {"error": "Both workspace_id and task_category_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        connections = workspace_category_option.objects.filter(
            workspace = workspace_id,
            task_category = task_category_id,
            category_option = category_option_id
        )
        connections.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get_serializer_class(self):
    #     # can also check if POST: if self.request.method == 'POST
    #     if self.action == 'create' or self.action == 'update':
    #         return CreateOption
    #     return super().get_serializer_class()

#####TODO(if ther is workspace_id in the Task_Category Model and the related_name is category__workspace)
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if 'HTTP_AUTHORIZATION' in self.request.META:
    #         if not self.request.user.is_staff:
    #             # Either filter directly by workspace if the model has the field
    #             # Or filter through the related Task_Categories
    #             user_workspace = self.request.user.workspace
    #             qs = qs.filter(category__workspace=user_workspace) 
    #     return qs




# class TaskCategoryViewSet(viewsets.ModelViewSet):
#     queryset = Task_Category.objects.all()
#     serializer_class = TaskCategorySerializer
#     permission_classes = [
#         IsAuthenticated,
#         # IsCliet, TODO
#     ]

#####TODO(if ther is workspace_id in the Task_Category Model)
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if 'HTTP_AUTHORIZATION' in self.request.META:
    #         if not self.request.user.is_staff:
    #             # Filter by workspace - adjust field names based on your actual model
    #             user_workspace = self.request.user.workspace
    #             qs = qs.filter(workspace=user_workspace)
    #     return qs


# class AssignOptionsToCategoryAPIView(generics.CreateAPIView):
#     model = workspace_category_option
#     serializer_class = AssignOptionsToCategorySerializer



class TaskCategoryViewSet(viewsets.ModelViewSet):
    queryset = Task_Category.objects.all()
    serializer_class = TaskCategorySerializer
    permission_classes = [
        IsAuthenticated,
        # IsCliet, TODO
    ]

    def get_serializer_class(self):
        if self.action == 'assign_to_workspace':
            return WorkspaceCategoryAssignmentSerializer
        elif self.action == 'add_options':
            return WorkspaceCategoryOptionAssignmentSerializer
        return super().get_serializer_class() 
    
    def get_queryset(self):
        qs = super().get_queryset()
        # if 'HTTP_AUTHORIZATION' in self.request.META:
        #     if not self.request.user.is_staff:
        #         # Filter by workspace - adjust field names based on your actual model
        #         user_workspace = self.request.user.workspace
        #         qs = qs.filter(workspace=user_workspace)
        workspace_id = Users_Workspaces.objects.filter(user = self.request.user).first()
        task_category_id = workspace_category_option.objects.filter(workspace = workspace_id.workspace).values_list('task_category', flat=True)
        qs = qs.filter(id__in = task_category_id)
        return qs

    @action(detail=False, methods=['post'], url_path='assign-to-workspace')
    def assign_to_workspace(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], url_path='add-options')
    def add_options(self, request):
        print(f"\n\n\n{request.data}\n\n\n")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=['put'], url_path='update-option')
    def update_option(self, request):
        serializer = UpdateCategoryOptionSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        
        option = serializer.validated_data['option']
        
        updated_option = serializer.update(option, serializer.validated_data)
        
        return Response(serializer.to_representation(updated_option))
    

    @action(detail=False, methods=['patch'], url_path='update-category')
    def update_category(self, request):
        serializer = UpdateTaskCategorySerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Get the category instance from validated data
        task_category = serializer.validated_data['task_category']
        
        # Perform the update
        updated_category = serializer.update(task_category, serializer.validated_data)
        
        return Response(serializer.to_representation(updated_category))
    

    def destroy(self, request, *args, **kwargs ):
        workspace_id = request.data.get('workspace')
        task_category_id = request.data.get('task_category')
        if not workspace_id or not task_category_id:
            return Response(
                {"error": "Both workspace_id and task_category_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        connections = workspace_category_option.objects.filter(
            workspace = workspace_id,
            task_category = task_category_id
        )
        connections.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)