from rest_framework import generics, mixins, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSatffEditorPermission
from api.authentication import TokenAuthentication, ExpiringTokenAuthentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [
        authentication.SessionAuthentication, 
        # TokenAuthentication, # Our overriden version of the built-in class with that name
        ExpiringTokenAuthentication # With a new ExpiringToken model underneath it
    ] 
    permission_classes = [permissions.IsAuthenticated, IsSatffEditorPermission]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None: 
            content = title
        serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_filed = 'pk' 

product_detail_view = ProductDetailAPIView.as_view()

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_filed = 'pk' # that is default value anyway
 
    def perform_update(self, serializer):
        instance = serializer.save() 

product_update_view = ProductUpdateAPIView.as_view()

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_filed = 'pk' 

    def perform_destroy(self, instance):
        # ...
        return super().perform_destroy(instance)

product_delete_view = ProductDeleteAPIView.as_view()


# A combined class view for the views above
# Maybe not the best way to go but still cool (can always look-up class definitions with Vs Code --> Go to Definition)
class ProductMixinView(
                    mixins.ListModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or None
        if content is None: 
            content = 'This is a single mixin view doing cool stuff'
        serializer.save(content=content)
    
product_mixin_view = ProductMixinView.as_view()



# A combined function view for the views above
@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method # PUT --> update, DESTROY --> delete

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)


    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None: 
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
