"""
URL configuration for Events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from rest_framework import permissions
from django.urls import include, path
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Events API",
        default_version='v1',
        description="Documentation de l'API des événements",
        contact=openapi.Contact(email="presira857@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/events/", include("apis.events.urls")),
    path("api/halls/", include("apis.halls.urls")),
    path("tickets/", include("apis.tickets.urls")),
    path("api/users/", include("apis.users.urls")),
    path('', include('apps.home.urls')),
    path('search/', include('apps.search.urls')),
    
     # Swagger endpoints
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
 
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    