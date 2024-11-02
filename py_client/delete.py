import requests

product_id = input("What product ID do you want to use?")
try:
    product_id = int(product_id)
except:
    print(f'{product_id} is not a valid Product ID')
    product_id = None

if product_id:
    endpoint = f"http://127.0.0.1:8000/api/products/{product_id}/delete"
    response = requests.delete(endpoint)
    print(response.status_code, response.status_code==204)