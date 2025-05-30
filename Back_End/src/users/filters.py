import django_filters
from .models import User

class UserFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    updated_at = django_filters.DateFilter(field_name='updated_at__date')
    class Meta:
        model= User
        fields = {
            'fullname': ['exact' , 'iexact' , 'icontains'],
            'email': ['exact' , 'iexact' , 'icontains'],
            'created_at': ['exact' , 'lt' , 'gt' , 'range'],
            'updated_at': ['exact' , 'lt' , 'gt' , 'range'],
        }