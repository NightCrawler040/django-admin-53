# Importing necessary modules from Django and Django REST framework
from django.forms import ValidationError
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, WishList
from .serializers import CategorySerializer, ProductSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


# ViewSet for handling CRUD operations on the Category model
class CategoryViewSet(viewsets.ModelViewSet):
    # Queryset containing all Category objects
    queryset = Category.objects.all()
    # Serializer class for Category model
    serializer_class = CategorySerializer
    # Filter backend for CategoryViewSet
    filter_backends = [DjangoFilterBackend]
    # Fields available for filtering in the CategoryViewSet
    filterset_fields = {
        'id': ['exact'],
        'title': ['exact']
    }


# ViewSet for handling CRUD operations on the Product model
class ProductViewSet(viewsets.ModelViewSet):
    # Queryset containing all Product objects
    queryset = Product.objects.all()
    # Serializer class for Product model
    serializer_class = ProductSerializer
    # Filter backends for ProductViewSet
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Fields available for filtering in the ProductViewSet
    filterset_fields = {
        'id': ['exact'],
        'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
        'title': ['exact'],
        'category': ['exact']
    }
    # Fields available for ordering in the ProductViewSet
    ordering_fields = ['title', 'price']
    # Default ordering for the ProductViewSet
    ordering = ['title']
    # Fields available for search in the ProductViewSet
    search_fields = ['title']


# View for user registration
class RegisterView(APIView):
    def post(self, request):
        # Creating a UserSerializer instance with the request data
        serializer = UserSerializer(data=request.data)
        # Validating the serializer data, raising an exception if invalid
        serializer.is_valid(raise_exception=True)
        # Saving the user data
        serializer.save()
        # Returning the serialized user data in the response
        return Response(serializer.data)


# View for handling operations related to the user's wish list
class WishListView(APIView):
    def get(self, request):
        # Retrieving the user's wish list and returning the product IDs
        wish_list = WishList.objects.filter(user=self.request.user.id).values_list('product', flat=True)
        return Response(wish_list)

    def post(self, request):
        # Getting the product ID from the request data
        product_id = request.data.get('product_id')
        # Validating the presence of the product ID
        if not product_id:
            raise ValidationError('Product id is required')

        # Checking if the user has an existing wish list
        if not WishList.objects.filter(user=self.request.user).exists():
            # Creating a new wish list with the user and adding the product
            wish_list = WishList.objects.create(user=self.request.user)
            wish_list.product.add(product_id)
        else:
            # Adding the product to the existing wish list
            wish_list = WishList.objects.get(user=self.request.user)
            wish_list.product.add(product_id)
        # Returning a success response
        return Response({'status': 'success'})

    def delete(self, request):
        # Getting the product ID from the request data
        product_id = request.data.get('product_id')
        # Validating the presence of the product ID
        if not product_id:
            raise ValidationError('Product id is required')
        # Removing the product from the user's wish list
        wish_list = WishList.objects.get(user=self.request.user)
        wish_list.product.remove(product_id)
        # Returning a success response
        return Response({'status': 'success'})
