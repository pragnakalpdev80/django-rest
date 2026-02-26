"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# core/urls.py
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # POST /api/token/ - Get tokens (login)
    TokenRefreshView,     # POST /api/token/refresh/ - Get new access token
    TokenVerifyView,      # POST /api/token/verify/ - Check if token is valid
)
from strawberry.django.views import GraphQLView
from api.schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('api/v1/', include(('api.urls', 'api'), namespace='v1')),
    # path('api/v2/', include(('api.urls', 'api'), namespace='v2')),
    # JWT authentication endpoints
    # POST /api/token/ - Login: Send username/password, get access+refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # POST /api/token/refresh/ - Refresh: Send refresh token, get new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # POST /api/token/verify/ - Verify: Send token, check if it's valid
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('graphql/', GraphQLView.as_view(schema=schema))
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    except ImportError:
        pass