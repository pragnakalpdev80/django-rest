import django_filters
from rest_framework.filters import BaseFilterBackend
from .models import Book, Task

class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['author', 'created_after', 'created_before']


class TaskFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY)
    created_after = django_filters.DateFilter(field_name='create' \
    'd_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta: 
        model = Task
        fields = ['priority', 'created_at', 'created_after']


class CustomFilterBackend(BaseFilterBackend):
    """
    Custom filter backend for complex filtering logic.
    """
    def filter_queryset(self, request, queryset, view):
        # Add custom filtering logic here
        if request.query_params.get('my_custom_filter'):
            queryset = queryset.filter(...)
        return queryset