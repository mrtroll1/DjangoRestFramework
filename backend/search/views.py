from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs =  super().get_queryset()
        q = self.request.GET.get('q')
        if q is None:
            return qs
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
        return qs.search(query=q, user=user)