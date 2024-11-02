import requests

product_id = input("What product ID do you want to use?")
try:
    product_id = int(product_id)
except:
    print(f'{product_id} is not a valid Product ID')
    product_id = None

if product_id:
    endpoint = f"http://127.0.0.1:8000/api/products/{product_id}/update"

    data = {
        "title": "Title updated with PUT request",
        "price": 70.99,
    }

    response = requests.put(endpoint, json=data)
    print(response.json())