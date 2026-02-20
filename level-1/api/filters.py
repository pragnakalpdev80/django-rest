import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(lookup_expr='icontains')
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['author', 'created_after', 'created_before']