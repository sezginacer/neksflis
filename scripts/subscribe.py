import requests

base_url = 'http://localhost:8080'


def login():
    data = dict(
        username='john.adams',
        password='password'
    )
    response = requests.post(f'{base_url}/account/token/', json=data)
    assert response.ok
    return response.json()['token']


def run():
    auth_key = login()
    response = requests.post(
        url=f'{base_url}/subscription/subscribe/',
        json=dict(
            plan='gold',
            payment_option='xyz',
            credit_card=dict(
                number='5586125903245963',
                expiry='2021/12',
                security_code='123'
            )
        ),
        headers=dict(Authorization=f'Token {auth_key}'),
    )
    assert response.ok
