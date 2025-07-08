from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apiApp.models import CustomUser, Product, Category


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    ordering = ('price',)
    search_fields = ('name',)
    list_filter = ('category',)
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ('name',)
admin.site.register(Category, CategoryAdmin)
