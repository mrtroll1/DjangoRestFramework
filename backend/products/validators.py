from django.apps import apps
from django.core.exceptions import ValidationError

def validate_title(value):
    Product = apps.get_model('products', 'Product')
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise ValidationError("A product with this title already exists")
    return value