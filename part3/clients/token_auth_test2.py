import requests
from pprint import pprint


def client():
    token = 'Token 022d2bc51958c9c5cbc435cd70b8a1c994f6ebc2'

    headers = {

    'Authorization': token,

    }

    response = requests.get(
        url='http://127.0.0.1:8000/api/kullanici-profilleri/',
        headers=headers,

    )

    print('Status Code:', response.status_code)

    response_data = response.json()
    pprint(response_data)


if __name__ == '__main__':
    client()
