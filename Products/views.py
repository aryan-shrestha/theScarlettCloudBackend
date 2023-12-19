from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from Products.models import Category, Product
from Products.serializers import CategorySerializer, ProductSerializer, CategoryProductListSerializer


# Create your views here.

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-dis_percentage')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug']
    search_fields = ['name', 'slug']
    ordering_fields = ['name','og_price']

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoryProductList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductListSerializer
