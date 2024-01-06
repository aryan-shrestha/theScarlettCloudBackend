from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Category
from .serializers import CategorySerializer
# Create your views here.

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]