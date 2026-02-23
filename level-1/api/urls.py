# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'products', views.ProductViewSet, basename='product')
# level-3
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'comments',views.CommentViewSet, basename='comment')
router.register(r'tasks3', views.Task3ViewSet, basename='task3')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'priorities', views.PriorityViewSet, basename='priority')

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    # path("login/",views.LoginView.as_view(),name="login"),
    # path("logout/",views.LogoutView.as_view(),name="logout")
    path('user-profile/', views.CreateUserView.as_view(), name='profile'),  
]