from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from cloudinary import CloudinaryImage

from Products.models import Product, ProductImages, Category
from category.serializers import CategorySerializer

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:     
        model= ProductImages
        fields = ['image']
    
    def get_image(self, obj):
        return CloudinaryImage(obj.image.url).build_url()

class ProductSerializer(WritableNestedModelSerializer):
    images = ProductImageSerializer(many=True)
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'og_price', 'dis_price', 'stock', 'dis_percentage', 'created_at', 'modified_at', 'images']
    
class CategoryProductListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['name','slug' ,'products']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = sorted(representation['products'], key=lambda x: x['dis_percentage'], reverse=True)

        return representation