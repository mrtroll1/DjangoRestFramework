# A file for Algolia Search API package to track models
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from.models import Product

# We want to define what EXACTLY to share with Angolia 
# Run angolia_reindex management command for changes to this class to take effect
@register(Product)
class ProductIndex(AlgoliaIndex):
    should_index = 'is_public' # Changes to is_public field of records immideately reflect on the Algolia side
    fields = [
        'title',
        'content',
        'price',
        'user',
        'public'
    ]