from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field='pk')
    email = serializers.EmailField(write_only=True) # there is no such filed in the Product model and it's ok since we override 'create' method
    class Meta:
        model = Product
        fields = [
            'pk',
            'url',
            'edit_url',
            'title',
            'content',
            'price',
            'email',
        ]

    def create(self, validated_data):
        # email = validated_data.pop('email')
        # obj = super().create(validated_data)

        # ... 
        # Maybe some email sending logic (like confirm purchase) without storing it

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        return super().update(instance, validated_data)
    
    def get_edit_url(self, obj):
        request = self.context.get('request') #serializers do not always have requests
        if request is None:
            return None

        return reverse('product-edit', kwargs={'pk': obj.pk}, request=request)
    

class ProductDetailSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field='pk')
    class Meta:
        model = Product
        fields = [
            'pk',
            'url',
            'edit_url',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]

    def get_my_discount(self, obj):
        # can define many custom logics here using obj and its properties:
        # obj.user --> user.username ... 
        # obj.category ...
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
    
    def get_edit_url(self, obj):
        request = self.context.get('request') #serializers do not always have requests
        if request is None:
            return None

        return reverse('product-edit', kwargs={'pk': obj.pk}, request=request)