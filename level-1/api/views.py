from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.views import exception_handler
from .models import Book,Task
from .serializers import BookSerializer, TaskSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
        
#         # Custom response
#         return Response({
#             'success': True,
#             'message': 'Task created successfully',
#             'data': serializer.data
#         }, status=status.HTTP_201_CREATED)
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
        
#         return Response({
#             'count': queryset.count(),
#             'results': serializer.data
#         })


# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
    
#     if response is not None:
#         custom_response_data = {
#             'error': 
#                 {'status_code': response.status_code,
#                 'message': 'An error occurred',
#                 'details': response.data}}
#         response.data = custom_response_data
    
#     return response


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