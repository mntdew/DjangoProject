from django.contrib import admin
from .models import Category, Project, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']