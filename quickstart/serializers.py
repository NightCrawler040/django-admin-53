# Importing necessary modules from the Django REST framework
from rest_framework import serializers
# Importing models from the current Django app
from .models import Category, Product, UserData


# Serializer for the Product model, using the ModelSerializer provided by Django REST framework
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Specifying the model to be serialized
        model = Product
        # Specifying the fields to include in the serialized output
        fields = ['id', 'title', 'price', 'category', 'description', 'image']


# Serializer for the Category model, using the ModelSerializer provided by Django REST framework
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # Specifying the model to be serialized
        model = Category
        # Specifying the fields to include in the serialized output
        fields = ['id', 'title']


# Serializer for the UserData model, using the ModelSerializer provided by Django REST framework
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Specifying the model to be serialized
        model = UserData
        # Specifying the fields to include in the serialized output
        fields = ["id", "email", "name", "password"]

    # Overriding the create method to handle user creation with password hashing
    def create(self, validated_data):
        # Creating a new UserData instance with the provided email and name
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                       )
        # Setting the password for the user and hashing it
        user.set_password(validated_data['password'])
        # Saving the user instance to the database
        user.save()
        # Returning the created user
        return user
