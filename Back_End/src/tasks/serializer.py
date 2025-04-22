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
    class OptionIdSerializer(serializers.ModelSerializer):
        # class OptionSerializer(serializers.ModelSerializer):
        #     class Meta:
        #         model = Category_Option
        #         fields = ['name']
        # name = OptionSerializer(many = False)
        class Meta:
            model = workspace_category_option
            fields = ['category_option' ]
    options = OptionIdSerializer(many = True)
    class Meta:
        model = Task_Category
        fields = ['id', 'name' , 'options']
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
    class UsersTasksSerializer(serializers.ModelSerializer):
        class Meta:
            model = users_tasks
            fields = ['user']


    users_task = UsersTasksSerializer(many = True)
    items = TasksTaskCategorySerializer(many = True , read_only = True)
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'out_dated',
            'created_at',
            'updated_at',
            'workspace_id',
            'owner_id',
            'image',
            'items',
            'users_task',
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


    users_task = UsersTasksSerializer(many = True)
    items = TasksTaskCategoryCreateSerializer(many = True)
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'start_date',
            'end_date',
            # 'out_dated',
            'workspace',
            'owner',
            'image',
            'items',
            'users_task'
        )
        extra_kwargs = {
            'image': {'required': False}
        }
        # extra_kwargs = {
        #     'owner': {'read_only': True}
        # }

    def create(self, validated_data):
        task_data = validated_data.pop('items')
        task_user = validated_data.pop('users_task')

        with transaction.atomic():
            task = Task.objects.create(**validated_data)

            # new line code to verification

            for data in task_data:
                if not workspace_category_option.objects.filter(
                    workspace = validated_data['workspace'],
                    task_category = data['task_category'],
                    category_option = data['category_option']
                ).exists():
                    raise serializers.ValidationError(
                    "This option is not assigned to the specified workspace and category"
                    )
                
            #############

            for data in task_data:
                tasks_task_categories.objects.create(task = task , **data)

                    
            for user in task_user:
                users_tasks.objects.create(task = task , **user)

        return task
    

    def update(self, instance, validated_data):
        task_data = validated_data.pop('items')
        # if instance.valid_for_edit():
        task_user = validated_data.pop('users_task')
        instance = super().update(instance , validated_data)

        if task_user is not None:
            instance.users_task.all().delete()

        for user in task_user:
                users_tasks.objects.create(task = instance , **user)


        # Category_Option.objects.get(task_data.items.category_option)      


        if task_data is not None:
            instance.items.all().delete()



            for data in task_data:
                if not workspace_category_option.objects.filter(
                        workspace = validated_data['workspace'],
                        task_category = data['task_category'],
                        category_option = data['category_option']
                    ).exists():
                        raise serializers.ValidationError(
                        "This option is not assigned to the specified workspace and category"
                        )
                
            ###############################

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

    def validate_name(self, value):
        return value.lower() 

    def create(self, validated_data):
        workspace = validated_data.pop('workspace')
        name = self.validate_name(validated_data['name'])

        # if  Task_Category.objects.filter(name = self.name).exists():
        #     category = Task_Category.objects.get(name = self.name)
        #     workspace_category_option.objects.create(
        #         workspace=workspace,
        #         task_category=category,
        #         category_option=None
        #     )
        #     return category

        try:
            category = Task_Category.objects.get(name__iexact=name)
        except Task_Category.DoesNotExist:
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
    workspace = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        # source='workspace'
    )
    task_category = serializers.PrimaryKeyRelatedField(
        queryset=Task_Category.objects.all(),
        # source='task_category'
    )
    options = CategoryOptionSerializer(many=True)

    # def validate(self, data):
        
    #     if not workspace_category_option.objects.filter(
    #         workspace=data['workspace'],
    #         task_category=data['task_category'],
    #         category_option=None
    #     ).exists():
    #         raise serializers.ValidationError(
    #             "This category is not assigned to the specified workspace"
    #         )
    #     return data

    def create(self, validated_data):
        workspace = validated_data['workspace']
        task_category = validated_data['task_category']
        options_data = validated_data['options']
        
        

        created_options = []

        # workspace_category_option.objects.get_or_create(
        #     workspace=workspace,
        #     task_category=task_category,
        #     category_option=None
        # )

        for option_data in options_data:
        
            option_name = option_data.get('name', '').strip().lower()
            
            
            option, created = Category_Option.objects.get_or_create(
                name__iexact=option_name,
                # task_category=task_category,
                defaults={'name':option_name}
            )
            
            # print(option_name)

            
            workspace_category_option.objects.get_or_create(
                workspace=workspace,
                task_category=task_category,
                category_option=option,
                # defaults={}  
            )
            
            created_options.append(option)

        return {
            'workspace_id': workspace.id,
            'task_category_id': task_category.id,
            'options': created_options
        }
    


    def to_representation(self, instance):
        return {
            'workspace_id': instance['workspace_id'],
            'task_category_id': instance['task_category_id'],
            'options': CategoryOptionSerializer(instance['options'], many=True).data
        }
    
class UpdateCategoryOptionSerializer(serializers.Serializer):
        workspace = serializers.PrimaryKeyRelatedField(
            queryset=Workspace.objects.all(),
            # source='workspace'
        )
        task_category = serializers.PrimaryKeyRelatedField(
            queryset=Task_Category.objects.all(),
            # source='task_category'
        )
        option = serializers.PrimaryKeyRelatedField(
            queryset=Category_Option.objects.all(),
            # source='option'
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

        def validate_name(self, value):
            return value.lower() 


        def update(self, instance, validated_data):
            validated_data['name'] = self.validate_name(validated_data['name'])

            existing_option = Category_Option.objects.filter(name__iexact=validated_data['name']).first()
            if existing_option and existing_option.id !=instance.id:
                connections = workspace_category_option.objects.filter(workspace =  validated_data['workspace'] , task_category= validated_data['task_category'] , category_option = instance)
                connections.update(category_option = existing_option)
                # for connection in connections:
                #     connection.update(task_category = existing_option)
                return existing_option
            else:
                option_all = Category_Option.objects.create(name = validated_data['name'])
                
                # for option_one in option_all:

                workspace_category_option.objects.update(
                        workspace=instance.workspace,
                        task_category=instance.category,
                        # category_Option = option_one
                        category_option = option_all
                    )
            # return option_all

            # instance.name = validated_data.get('name', instance.name)
            # instance.save()
            # return instance

        def to_representation(self, instance):
            return {
                'id': instance.id,
                'name': instance.name,
                'workspace_id': self.validated_data['workspace'].id,
                'task_category_id': self.validated_data['task_category'].id
            }


class UpdateTaskCategorySerializer(serializers.Serializer):
    workspace = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        # source='workspace'
    )
    task_category = serializers.PrimaryKeyRelatedField(
        queryset=Task_Category.objects.all(),
        # source='category'
    )
    name = serializers.CharField(max_length=20, required=True)

    def validate(self, data):
        if not workspace_category_option.objects.filter(
            workspace=data['workspace'],
            task_category=data['task_category'],
            # category_option=None  
        ).exists():
            raise serializers.ValidationError(
                "This category is not assigned to the specified workspace"
            )
        return data

    def validate_name(self, value):
        return value.lower() 

    def update(self, instance, validated_data):
        validated_data['name'] = self.validate_name(validated_data['name'])

        
        existing_category = Task_Category.objects.filter(name__iexact=validated_data['name']).first()
        if existing_category and existing_category.id !=instance.id:
            
            connections = workspace_category_option.objects.filter(workspace = validated_data['workspace'] , task_category=instance)
            connections.update(task_category = existing_category)
            # for connection in connections:
            #     connection.update(task_category = existing_category)
            return existing_category
        else:
            categories = Task_Category.objects.create(name = validated_data['name'])
            # for category in categories:
            workspace_category_option.objects.update(
                    workspace=instance.workspace,
                    # task_category=category
                    task_category = categories
            )
        
            return categories
            
            # return category

        # instance.name = validated_data.get('name', instance.name)
        # instance.save()
        # return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'workspace_id': self.validated_data['workspace'].id
        }