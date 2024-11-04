from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field='pk', read_only=True)
    title = serializers.CharField(read_only=True)

class UserPublicSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    three_other_products = serializers.SerializerMethodField(read_only=True)

    def get_three_other_products(self, obj):
        user = obj
        user_products_qs = user.product_set.all()[:3]

        request = self.context.get('request')
        if request is None:
            return UserProductInlineSerializer(user_products_qs, many=True).data
        
        return UserProductInlineSerializer(user_products_qs, many=True, context={'request': request}).data