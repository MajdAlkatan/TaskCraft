import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    updated_at = django_filters.DateFilter(field_name='updated_at__date')
    start_date = django_filters.DateFilter(field_name='start_date__date')

    class Meta:
        model = Task
        fields = {
            'title': ['exact' ,'iexact' , 'icontains'],
            'created_at': ['exact' , 'lt' , 'gt' , 'range'],
            'updated_at': ['exact' , 'lt' , 'gt' , 'range'],
            'start_date': ['exact' , 'lt' , 'gt' , 'range'],
        }