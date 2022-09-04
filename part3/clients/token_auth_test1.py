import requests
from pprint import pprint

#{'key':'ad101c93fb7cdfd3e535d075dac3893fb7f9e949'}
def client():
    credentials = {
        'username': 'test_user',
        'password': 'test123456'
    }

    response = requests.post(
        url='http://127.0.0.1:8000/api/dj-rest-auth/login/',
        data=credentials,
    )

    print('Status Code:', response.status_code)

    response_data = response.json()
    pprint(response_data)


if __name__ == '__main__':
    client()
