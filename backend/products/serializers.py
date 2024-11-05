from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from .validators import validate_title

from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field='pk')
    email = serializers.EmailField(write_only=True) # there is no such filed in the Product model and it's ok since we override 'create' method
    # user_id = serializers.CharField(source='user.id', read_only=True) # if a user forign key was attached to Product model
    # title = serializers.CharField(validators=[validate_title]) # it is better to put validators on models tho (do use them if request.context is important)

    class Meta:
        model = Product
        fields = [
            'pk',
            'url',
            'edit_url',
            'title',
            'user',
            'content',
            'price',
            'public',
            'email',
        ]

    # Ensure user-unique title 
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title_iexact=value)
    #     if qs.exists():
    #         return serializers.ValidationError('A product with this title already exists')
    #     return value


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
    # my_user_data = serializers.SerializerMethodField(read_only=True) # Use separate UserPublicSerializer instead of serializing related data
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field='pk')
    owner = UserPublicSerializer(source='user', read_only=True) 

    class Meta:
        model = Product
        fields = [
            'pk',
            'url',
            'edit_url',
            'title',
            'owner',
            'content',
            'price',
            'public',
            'sale_price',
            'my_discount',
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