# api/serializers.py
from rest_framework import serializers
from .models import Book, Task


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn']

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'published_date', 'isbn', 'description', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'desc', 'completed', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']



# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'published_date', 'isbn', 'created_at','is_deleted']
#         # Or use '__all__' to include all fields
#         # fields = '__all__'
        
#         # Exclude specific fields
#         # exclude = ['created_at']
        
#         # Read-only fields
#         read_only_fields = ['id', 'created_at']


# class BookSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=200)
#     author = serializers.CharField(max_length=100)
#     published_date = serializers.DateField()
#     isbn = serializers.CharField(max_length=13)
#     created_at = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         """Create and return a new Book instance"""
#         return Book.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """Update and return an existing Book instance"""
#         instance.title = validated_data.get('title', instance.title)
#         instance.author = validated_data.get('author', instance.author)
#         instance.published_date = validated_data.get('published_date', instance.published_date)
#         instance.isbn = validated_data.get('isbn', instance.isbn)
#         instance.save()
#         return instance