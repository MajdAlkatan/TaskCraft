from rest_framework import serializers
from .models import Task , users_tasks , Task_Category , Category_Option , tasks_task_categories
from django.db import transaction

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
        fields = ('id' , 'name' , 'task_category')
        extra_kwargs = {
            'id': {'read_only': True}
        }

class TaskCategorySerializer(serializers.ModelSerializer):
    options = CategoryOptionSerializer(many = True)
    class Meta:
        model = Task_Category
        fields = ('id' , 'name' , 'options')
        extra_kwargs = {
            'id': {'read_only': True},
            'options': {'read_only': True}
        }

class TaskCategoryCreateSerializer(serializers.ModelSerializer):
    options = CategoryOptionSerializer(many = True)
    class Meta:
        model = Task_Category
        fields = ('name' , 'options')

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
            # 'owner_tasks',
            'items',
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    class TasksTaskCategoryCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = tasks_task_categories
            fields = ('task_category' , 'category_option')


    items = TasksTaskCategoryCreateSerializer(many = True)
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'start_date',
            'owner',
            'items',
        )
        # extra_kwargs = {
        #     'owner': {'read_only': True}
        # }

    def create(self, validated_data):
        task_data = validated_data.pop('items')

        with transaction.atomic():
            task = Task.objects.create(**validated_data)

            for data in task_data:
                tasks_task_categories.objects.create(task = task , **data)

        return task
    

    def update(self, instance, validated_data):
        task_data = validated_data.pop('items')
        instance = super().update(instance , validated_data)

        if task_data is not None:
            instance.items.all().delete()

            for data in task_data:
                tasks_task_categories.objects.create(task = instance , **data)
        return instance
    
    