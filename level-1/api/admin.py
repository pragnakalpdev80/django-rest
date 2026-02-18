from django.contrib import admin
from .models import Book,Task

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'published_date', 'created_at']
#     list_filter = ['created_at', 'published_date']
#     search_fields = ['title', 'author']

# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['title', 'desc', 'created_at']
#     list_filter = ['created_at', 'completed']
#     search_fields = ['title']