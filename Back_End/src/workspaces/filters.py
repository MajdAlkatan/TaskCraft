import django_filters
from .models import Workspace

class WorkspaceFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    updated_at = django_filters.DateFilter(field_name='updated_at__date')
    class Meta:
        model= Workspace
        fields = {
            'name': ['exact' , 'iexact' , 'contains' , 'icontains'],
            'owner': ['exact'],
        }