import requests

# endpoint = "https://httpbin.org"
# get_response = requests.get(endpoint)
# print(get_response.text)


# endpoint = "https://httpbin.org/anything"
# get_response = requests.get(endpoint, json={"query": "Hello World!"})
# print(get_response.json())
# print(get_response.status_code)
# print(get_response)

# endpoint = "http://127.0.0.1:8000"
# get_response = requests.get(endpoint)
# print(get_response.status_code)
# print(get_response.text)

# endpoint = "http://127.0.0.1:8000/api"
# get_response = requests.get(endpoint)
# print(get_response.status_code)
# print(get_response.text)
# print(get_response.json()['message'])

# endpoint = "http://127.0.0.1:8000/api"
# get_response = requests.get(endpoint, params={"abc": 123}, json={"query": "Hello World!"})
# print(get_response.json())

endpoint = "http://127.0.0.1:8000/api"
get_response = requests.post(endpoint, json={"title ": "New Product", "content": "Injested with a POST request", "price": 7.99})
print(get_response.json())