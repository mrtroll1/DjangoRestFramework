from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

# Not my favorite approach
# Viewsets handle all the http methods at url points pre-made by corrresponding routers
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer