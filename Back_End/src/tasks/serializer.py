from rest_framework import serializers
from .models import Task , users_tasks , Task_Category , Category_Option , tasks_task_categories , workspace_category_option
from workspaces.models import Workspace
from django.db import transaction



# class CreateOption(serializers.ModelSerializer):
#     class Option(serializers.ModelSerializer):
#         class Meta:
#             model = Category_Option
#             fields = ['id' , 'name']
#             extra_kwargs = {
#                 'id':{'read_only': True}
#             }

#     options = Option(many = True)
#     # category_option = serializers.ModelSerializer(source = "options.id")
#     class Meta:
#         model = workspace_category_option
#         fields = ('id' , 'workspace' , 'task_category' , 'options' )
#         # extra_kwargs = {
#         #     'category_option':{'read_only': True}
#         # }

class WorkspaceCategoryOptionSerializer(serializers.ModelSerializer):
    # option_name = serializers.CharField(source = 'category_option.name')
    class Meta:
        model = workspace_category_option
        fields = ('id' , 'workspace' , 'task_category' , 'category_option')
        extra_kwargs = {
            'id': {'read_only': True},
            'category_option': {'read_only': True}
        }
class UserTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_tasks
        fields = ('user')


class TasksTaskCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = 'task_category.name')
    option_name = serializers.CharField(source = 'category_option.name')
    class Meta:
        model = tasks_task_categories
        fields = (
            # 'task',
            'category_name',
            'option_name',
            # 'task_category',
            # 'Category_option',
        )

class CategoryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Option
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True}
        }

# class TaskCategorySerializer(serializers.ModelSerializer):
#     options = WorkspaceCategoryOptionSerializer(many = True)
#     class Meta:
#         model = Task_Category
#         fields = ('id' , 'name' , 'options')
#         extra_kwargs = {
#             'id': {'read_only': True},
#             'options': {'read_only': True}
#         }

class TaskCategorySerializer(serializers.ModelSerializer):

    # options = CategoryOptionSerializer(many=True, required=False)
    
    class Meta:
        model = Task_Category
        fields = ['id', 'name' ]
        extra_kwargs = {'id': {'required': False}}


# class AssignOptionsToCategorySerializer(serializers.ModelSerializer):
#     class OptionSeriazer(serializers.ModelSerializer):
#         class Meta:
#             model = Category_Option
#             fields = ('id' , 'name')
#     options = OptionSeriazer(many = True)
#     class Meta:
#         model = workspace_category_option
#         fields = ('task_category' , 'options')



    # def create(self, validated_data):
    #     options_data = validated_data.pop('options', [])
    #     task_category = Task_Category.objects.create(**validated_data)
        
    #     for option_data in options_data:
    #         option, _ = Category_Option.objects.get_or_create(**option_data)
    #         task_category.options.add(option)
            
    #     return task_category

class TaskSerializer(serializers.ModelSerializer):
    # owner_tasks = UserTasksSerializer(many = True , read_only = True)
    items = TasksTaskCategorySerializer(many = True , read_only = True)
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'created_at',
            'updated_at',
            'owner_id',
            'image',
            # 'user',
            # 'owner_tasks',
            'items',
        )
        # extra_kwargs = {
        #     'image': {'required': False}
        # }


class TaskCreateSerializer(serializers.ModelSerializer):
    class TasksTaskCategoryCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = tasks_task_categories
            fields = ('task_category' , 'category_option')
    
    class UsersTasksSerializer(serializers.ModelSerializer):
        class Meta:
            model = users_tasks
            fields = ['user']


    users = UsersTasksSerializer(many = True)
    items = TasksTaskCategoryCreateSerializer(many = True)
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'start_date',
            'workspace'
            'owner',
            'image',
            'items',
            'users'
        )
        extra_kwargs = {
            'image': {'required': False}
        }
        # extra_kwargs = {
        #     'owner': {'read_only': True}
        # }

    def create(self, validated_data):
        task_data = validated_data.pop('items')
        task_user = validated_data.pop('users')

        with transaction.atomic():
            task = Task.objects.create(**validated_data)

            for data in task_data:
                tasks_task_categories.objects.create(task = task , **data)
            
            for user in task_user:
                users_tasks.objects.create(task = task , **user)

        return task
    

    def update(self, instance, validated_data):
        task_data = validated_data.pop('items')
        instance = super().update(instance , validated_data)

        if instance.valid_for_edit():
            task_user = validated_data.pop('users')
            for user in task_user:
                users_tasks.objects.create(task = instance , **user)


        # Category_Option.objects.get(task_data.items.category_option)      

        if task_data is not None:
            instance.items.all().delete()

            for data in task_data:
                tasks_task_categories.objects.create(task = instance , **data)
        return instance
    
    

class ChangeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['image']
        extra_kwargs = {
            'image': {'required': True}
        }



########################################




class WorkspaceCategoryAssignmentSerializer(serializers.Serializer):
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        source='workspace'
    )
    name = serializers.CharField(max_length=20)

    def create(self, validated_data):
        workspace = validated_data.pop('workspace')
        
        category = Task_Category.objects.create(**validated_data)
        
        workspace_category_option.objects.create(
            workspace=workspace,
            task_category=category,
            category_option=None
        )
        
        return category

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'workspace_id': self.validated_data['workspace'].id
        }
    



class WorkspaceCategoryOptionAssignmentSerializer(serializers.Serializer):
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        source='workspace'
    )
    task_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Task_Category.objects.all(),
        source='task_category'
    )
    options = CategoryOptionSerializer(many=True)

    def validate(self, data):
        
        if not workspace_category_option.objects.filter(
            workspace=data['workspace'],
            task_category=data['task_category'],
            category_option=None
        ).exists():
            raise serializers.ValidationError(
                "This category is not assigned to the specified workspace"
            )
        return data

    def create(self, validated_data):
        workspace = validated_data['workspace']
        task_category = validated_data['task_category']
        options_data = validated_data['options']
        
        created_options = []
        
        for option_data in options_data:
            
            option = Category_Option.objects.create(**option_data)
            

            workspace_category_option.objects.create(
                workspace=workspace,
                task_category=task_category,
                category_option=option
            )
            
            created_options.append(option)
        
        return {
            'workspace_id': workspace.id,
            'task_category_id': task_category.id,
            'options': created_options
        }
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        return {
            'workspace_id': instance['workspace_id'],
            'task_category_id': instance['task_category_id'],
            'options': CategoryOptionSerializer(instance['options'], many=True).data
        }
    
class UpdateCategoryOptionSerializer(serializers.Serializer):
        workspace_id = serializers.PrimaryKeyRelatedField(
            queryset=Workspace.objects.all(),
            source='workspace'
        )
        task_category_id = serializers.PrimaryKeyRelatedField(
            queryset=Task_Category.objects.all(),
            source='task_category'
        )
        option_id = serializers.PrimaryKeyRelatedField(
            queryset=Category_Option.objects.all(),
            source='option'
        )
        name = serializers.CharField(max_length=20)

        def validate(self, data):
            
            if not workspace_category_option.objects.filter(
                workspace=data['workspace'],
                task_category=data['task_category'],
                category_option=data['option']
            ).exists():
                raise serializers.ValidationError(
                    "This option is not assigned to the specified workspace and category"
                )
            return data

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance

        def to_representation(self, instance):
            return {
                'id': instance.id,
                'name': instance.name,
                'workspace_id': self.validated_data['workspace'].id,
                'task_category_id': self.validated_data['task_category'].id
            }


class UpdateTaskCategorySerializer(serializers.Serializer):
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        source='workspace'
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Task_Category.objects.all(),
        source='category'
    )
    name = serializers.CharField(max_length=20, required=False)

    def validate(self, data):
        if not workspace_category_option.objects.filter(
            workspace=data['workspace'],
            task_category=data['category'],
            category_option=None  
        ).exists():
            raise serializers.ValidationError(
                "This category is not assigned to the specified workspace"
            )
        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'workspace_id': self.validated_data['workspace'].id
        }