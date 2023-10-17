from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Define the API documentation schema view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapp.local"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)


from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Define your API URL patterns
app_patterns = [
    path('register/', views.UserRegisterationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('block/<int:id>/', views.BlockAPIView.as_view(), name='block'),
    # Add other app-specific URL patterns here
]

# Combine your app-specific URL patterns with the Swagger API documentation URL patterns
urlpatterns = [
    path('api/', include(app_patterns)),
    path('api/playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Optionally, you can add the Swagger UI documentation at the root URL
urlpatterns.append(path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'))

