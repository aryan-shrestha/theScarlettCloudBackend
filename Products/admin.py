from django.contrib import admin
import admin_thumbnails

from Products.models import Category, Product, ProductImages

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'category', 'og_price', 'dis_price', 'stock')
    prepopulated_fields = {'slug': ['name']}
    inlines = [ProductImagesInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImages)
