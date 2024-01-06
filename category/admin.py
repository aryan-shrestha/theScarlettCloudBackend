from django.contrib import admin

from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at')
    prepopulated_fields = {'slug': ['name']}

admin.site.register(Category, CategoryAdmin)
