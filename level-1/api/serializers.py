# api/serializers.py
import datetime
from rest_framework import serializers
from .models import Book, Task, Author, Product, UserProfile, Tag, Post, Comment, Task_3B, Priority, Category
from django.contrib.auth.models import User
from .validators import validate_titleletters

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'owner', 'description','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'published_date', 'isbn', 'description', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'desc', 'completed', 'priority', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'email']


class ProductSerializer(serializers.ModelSerializer):
    
    def validate(self,data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        if data['stock'] < 0:
            raise serializers.ValidationError("stock must be greater than or equal to 0")
        return data
        
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        
        def validate(self, data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords don't match")
            return data
        
        def create(self, validated_data):
            validated_data.pop('confirm_password')
            user = User.objects.create_user(**validated_data)
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['username','password', ]


class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)
    # email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields=['id','created_at']
        
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance = User.objects.get(
            username=user_data['username'])
        user_instance.save()
        
        user_profile_instance = UserProfile.objects.create(
            **validated_data, user=user_instance)
        user_profile.save()
        return user_profile

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id','created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id','created_at']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id','created_at']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)
        
        return post

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)        
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)
        
        return instance

class PrioritySerializer(serializers.ModelSerializer):

    def validate_priority(self,value):
        if not (value in Priority.LEVELS):
            raise serializers.ValidationError(f"{value} is not proper value for priority")
        return value

    class Meta:
        model = Priority
        fields = '__all__'
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

class Task3BSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_titleletters,])
    
    def validate_due_date(self,value):  
        if value <= datetime.date.today():
            raise serializers.ValidationError("Due date must be in future")
        return value
    
    class Meta:
        model = Task_3B
        fields = '__all__'
        read_only_fields = ['id']
        
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

    # def create(self, validated_data):
    #     categories = validated_data.pop('categories', [])
    #     priority_data = validated_data.pop('priority', None)
    #     task = Task.objects.create(**validated_data)
    #     if categories:
    #         task.categories.set(categories)
    #     if priority_data:
    #         Priority.objects.create(task=task, **priority_data)
    #     return task