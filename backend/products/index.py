# A file for Algolia Search API package to track models
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from.models import Product

# We want to define what EXACTLY to share with Angolia 
# Run angolia_reindex management command for changes to this class to take effect
@register(Product)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public' # Changes to is_public field of records immideately reflect on the Algolia side
    fields = [
        'pk',
        'title',
        # 'url', # has to be a field of Product model
        'content',
        'price',
        'user',
        'public'
    ]
    settings = {
        'searchableAttributes': ['title', 'content', 'tags'],
        'attributesForFaceting': ['public', 'user']
    }
    tags = 'get_tags_list' # to be used with algolia's built-in 'tags' search filter