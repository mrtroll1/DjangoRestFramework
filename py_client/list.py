import requests
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/auth/"
username = input("Username: ")
password = getpass()

auth_response = requests.post(auth_endpoint, json={
    "username": username,
    "password": password
})
print(auth_response.json())

if auth_response.status_code == 200:
    
    token = auth_response.json()['token']
    headers = {
        # "Authorization": f"Token {token}"
        "Authorization": f"Bearer {token}" # In api/authentication.py we override TokenAuthentication class and declare keyword = "Bearer"
    }

    
    next_url = 'http://127.0.0.1:8000/api/products/'
    page = 1

    while next_url:
        print(f'\nLoading page {page}.')
        endpoint = next_url
        response_json = requests.get(endpoint, headers=headers).json()

        print(f'Returning {len(response_json["results"])} / {response_json["count"]} items. \n')

        for result in response_json['results']:
            print(result)
        
        next_url = response_json['next']
        page += 1