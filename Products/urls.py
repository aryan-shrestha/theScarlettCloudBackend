from django.urls import path

from Products.views import CategoryList, ProductList, CategoryProductList, ProductDetail

urlpatterns = [
    path('category/products/', CategoryProductList.as_view(), name="category_product_list" ),
    path('', ProductList.as_view(), name='products_list'),
    path("<slug>/",  ProductDetail.as_view(), name='product_detail'),
]