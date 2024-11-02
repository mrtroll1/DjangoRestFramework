from django.http import JsonResponse
import json

# Create your views here.
# request is an instance of Djano HttpRequest Class
def api_home(request, *args, **kwargs):
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