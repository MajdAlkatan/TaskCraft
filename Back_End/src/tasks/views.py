from django.shortcuts import render
from rest_framework import viewsets , status , filters , generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from .models import Task , Category_Option , Task_Category , workspace_category_option
from .serializer import TaskSerializer , TaskCreateSerializer , CategoryOptionSerializer  ,TaskCategorySerializer , ChangeImageSerializer , WorkspaceCategoryAssignmentSerializer , WorkspaceCategoryOptionAssignmentSerializer , UpdateCategoryOptionSerializer , UpdateTaskCategorySerializer
from .filter import TaskFilter
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


    

    # def get_permissions(self):
    #     self.permission_classes = [AllowAny]
    #     if 'HTTP_AUTHORIZATION' in self.request.META:
    #         if not self.request.user.is_staff:
    #             self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TaskCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if 'HTTP_AUTHORIZATION' in self.request.META:
            if not self.request.user.is_staff:
                qs = qs.filter(owner = self.request.user.workspace)
                # qs = qs.filter(user = self.request.user)
        return qs
    
    @action(detail = True , methods = ['patch'] , serializer_class = ChangeImageSerializer)
    def change_image(self , request):
        serializer = self.get_serializer(data = request.data)
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


    @action(detail=False, methods=['post'], url_path='assign-to-workspace')
    def assign_to_workspace(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['post'], url_path='add-options')
    def add_options(self, request):
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
        category = serializer.validated_data['category']
        
        # Perform the update
        updated_category = serializer.update(category, serializer.validated_data)
        
        return Response(serializer.to_representation(updated_category))