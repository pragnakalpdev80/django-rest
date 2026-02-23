from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
from django.db.models import Count, Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics, filters
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Task, Author, Product, UserProfile, Post, Tag, Comment, Task_3B, Priority, Category
from .serializers import BookSerializer, TaskSerializer, AuthorSerializer, ProductSerializer, UserRegistrationSerializer, UserProfileSerializer, PostSerializer, CommentSerializer, TagSerializer, Task3BSerializer, PrioritySerializer, CategorySerializer
from .forms import RegistrationForm, LoginForm
from .permissions import IsOwnerOrReadOnly
from .throttles import BookCreateThrottle
from .filters import BookFilter, TaskFilter
from .pagination import BookLimitOffsetPagination


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = BookLimitOffsetPagination
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['title', 'author', 'published_date', 'created_at']
    search_fields = ['title', 'author', 'description']
    ordering = ['-created_at']

    def get_throttles(self):
        if self.action == 'create':
            return [BookCreateThrottle()]
        return super().get_throttles()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['title', 'priority', 'created_at']
    search_fields = ['title', 'desc']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Task created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'message': 'Task updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data  
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Post created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related('tags', 'comments').annotate(comment_count=Count('comments')).all()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Tag created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Comment created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Comment.objects.select_related('post','commenter').all()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        print(f"hello :-------------- {serializer}")
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,  # User information (username, email, etc.)
            'refresh': str(refresh),  # Refresh token (long-lived, used to get new access tokens)
            'access': str(refresh.access_token),  # Access token (short-lived, used for API requests)
        }, status=status.HTTP_201_CREATED)  # 201 = Created (successful resource creation)
    
class CreateUserView(generics.ListCreateAPIView):
    queryset =UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
  
class Task3ViewSet(viewsets.ModelViewSet):
    serializer_class = Task3BSerializer
    permission_classes = []

    def get_queryset(self):
        return (
            Task_3B.objects
            .select_related('assignee', 'priority')
            .prefetch_related('categories')
            .annotate(category_count=Count('categories'))
            .filter(Q(category_count__gte=1))
            .order_by('-created_at')
        )

class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Tag created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Priority.objects.prefetch_related('task').all()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response
        return Response({
            'success': True,
            'message': 'Tag created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# @action(detail=False, methods=['get'])
# def stats(self, request):
#     stats = Task.objects.aggregate(
#         total_tasks=Count('id'),
#         completed_tasks=Count('id', filter=Q(completed=True))
#     )
#     return Response(stats)
# category_count = serializers.IntegerField(read_only=True)
# class LoginView(LoginView):
#     template_name = 'api/login.html'
#     def get(self, request):
#         form= LoginForm()
#         return render(request, self.template_name, { 'form': form})

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         user = authenticate(username=username, password=password)
#         print(user)
#         if user is None:
#             messages.error(request,"Username or Password not matched")
#             return redirect('/api/login/')
#         login(request,user)
#         return redirect("/api/books/")
    

# class LogoutView(View):
#     def post(self,request):
#         if request.user.is_authenticated:
#             logout(request)
#             return redirect('/api/login/')


# class RegistrationView(View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect("/api/books/")
#         form = RegistrationForm()
#         return render(request, 'api/register.html', { 'form': form})  
    
#     def post(self, request):
#         form = RegistrationForm(request.POST)
#         print(request)
#         try:
#             if form.is_valid():
#                 print("valid")
#                 form.save()
#                 return redirect('/api/login/')   
#         except Exception as error:
#             print("invalid data")
#             print(error)
#         return redirect('/api/register/')     

# # api/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Book
# from .serializers import BookSerializer
# from django.http import Http404

# class BookListAPIView(APIView):
#     """List all books or create a new book"""
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BookDetailAPIView(APIView):
#     """Retrieve, update or delete a book"""
    
#     def get_object(self, pk):
#         try:
#             return Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404()
    
#     def get(self, request, pk):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         book = self.get_object(pk)
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         book = self.get_object(pk)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

