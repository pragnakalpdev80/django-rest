import django_filters
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
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta: 
        model = Task
        fields = ['priority', 'created_at', 'created_after']
