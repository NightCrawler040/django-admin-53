# Import necessary modules from Django
from django.contrib import admin
from .models import Category, Product, UserData

# Register the UserData model in the admin panel
admin.site.register(UserData)


# The @admin.register decorator is used to configure the display of the Category model in the admin panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Define fields to be displayed in the list of Category model objects
    list_display = ('id', 'title', 'created_at', 'updated_at')
    # Links to the details of the object in the list
    list_display_links = ('id', 'title')
    # Search field for quick searching of objects by title
    search_fields = ('title',)
    # Filters by title
    list_filter = ('title',)

    # Method to represent the object as a string
    def __str__(self) -> str:
        return self.title


# The @admin.register decorator for configuring the display of the Product model in the admin panel
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Define fields to be displayed in the list of Product model objects
    list_display = ('id', 'title', 'price', 'category', 'created_at', 'updated_at')
    # Links to the details of the object in the list
    list_display_links = ('id', 'title')
    # Search field for quick searching of objects by title
    search_fields = ('title',)
    # Filters by title
    list_filter = ('title',)

    # Method to represent the object as a string
    def __str__(self) -> str:
        return self.title
