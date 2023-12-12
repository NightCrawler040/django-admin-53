# Importing necessary modules from Django
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from quickstart import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Creating a router for automatic URL routing of viewsets
router = routers.DefaultRouter()
# Registering viewsets for the 'categories' and 'products' endpoints
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)

# Defining URL patterns for the Django project
urlpatterns = [
    # Including the automatically generated URLs for the viewsets using the router
    path('api/', include(router.urls)),
    # Admin panel URL
    path('admin/', admin.site.urls),
    # URL for user registration view
    path('api/register/', views.RegisterView.as_view(), name="sign_up"),
    # URL for JWT token generation (login)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # URL for JWT token refresh
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # URL for wish list view
    path('api/wishlist/', views.WishListView.as_view(), name='wishlist'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
