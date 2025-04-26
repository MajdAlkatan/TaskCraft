from django.db import models
from rest_framework.pagination import PageNumberPagination

#auto insert the created_at & updated_at fields
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=False , auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now=True , auto_now_add=False , editable=False)
    class Meta:
        abstract = True
    
class CustomPageNumberPaginator(PageNumberPagination):
    page_size = 50
    max_page_size = 120
    page_size_query_param = 'size'