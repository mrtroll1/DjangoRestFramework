from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from django.conf import settings

from products.models import Product
from products.serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
# request is an instance of Djano HttpRequest Class

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        
        return Response(serializer.data)
    

@api_view(["GET"])
def api_home_get(request, *args, **kwargs):
    """
    DRF API view
    """
    instance = Product.objects.all().order_by('?').first()
    data = {}
    if instance:
        data = ProductSerializer(instance).data
    return Response(data)

@api_view(["GET"])
def get_algolia_tokens(request, *args, **kwargs):
    """
    Endpoint to serve algolia App ID and Search-only token
    """
    algolia_app_id = settings.ALGOLIA['APPLICATION_ID']
    algolis_search_only_api_key = settings.ALGOLIA_SEARCH_ONLY_API_KEY
    data = {
        'AppID': algolia_app_id,
        'ApiKey': algolis_search_only_api_key
    }
    return Response(data)

    

def model_api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by('?').first() # get a random record
    data = {}
    if model_data:
        # The following will be done with Django serializers
        # Model instance --> Python dict --> JSON to serve to client

        # Manually
        # data['id'] = model_data.id
        # data['title'] = model_data.title
        # data['content'] = model_data.content
        # data['price'] = model_data.price

        # Using model_to_dict 
        data = model_to_dict(model_data, fields=['id', 'title'])
    return JsonResponse(data)


def basic_api_home(request, *args, **kwargs):
    body = request.body # assumed to be byte string of JSON data
    data = {}
    try:
        data = json.loads(body) # string of JSON data to Python Dict 
    except:
        pass
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse(data)