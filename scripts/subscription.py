import requests

base_url = 'http://localhost:8080'


def test_silver_user():
    data = dict(
        first_name='Silver',
        last_name='Adams',
        username='silver.adams',
        email='silver.adams@xyz.com',
        password='password'
    )
    response = requests.post(f'{base_url}/account/register/', json=data)
    assert response.ok

    auth_key = response.json()['token']
    headers = dict(Authorization=f'Token {auth_key}')

    response = requests.post(
        url=f'{base_url}/subscription/subscribe/',
        json=dict(
            plan='silver',
            payment_option='xyz',
            credit_card=dict(
                number='5586125903245963',
                expiry='2021/12',
                security_code='123'
            )
        ),
        headers=headers,
    )
    assert response.ok

    response = requests.get(url=f'{base_url}/content/silver/', headers=headers)
    assert response.ok

    response = requests.get(url=f'{base_url}/content/gold/', headers=headers)
    assert not response.ok
    assert response.status_code == 403

    response = requests.get(url=f'{base_url}/content/platinum/', headers=headers)
    assert not response.ok
    assert response.status_code == 403


def test_gold_user():
    data = dict(
        first_name='Gold',
        last_name='Adams',
        username='gold.adams',
        email='gold.adams@xyz.com',
        password='password'
    )
    url = f'{base_url}/account/register/'
    response = requests.post(url, json=data)
    assert response.ok

    auth_key = response.json()['token']
    headers = dict(Authorization=f'Token {auth_key}')

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
        headers=headers,
    )
    assert response.ok

    response = requests.get(url=f'{base_url}/content/silver/', headers=headers)
    assert response.ok

    response = requests.get(url=f'{base_url}/content/gold/', headers=headers)
    assert response.ok

    response = requests.get(url=f'{base_url}/content/platinum/', headers=headers)
    assert not response.ok
    assert response.status_code == 403


def test_platinum_user():
    data = dict(
        first_name='Platinum',
        last_name='Adams',
        username='platinum.adams',
        email='platinum.adams@xyz.com',
        password='password'
    )
    url = f'{base_url}/account/register/'
    response = requests.post(url, json=data)
    assert response.ok

    auth_key = response.json()['token']
    headers = dict(Authorization=f'Token {auth_key}')

    response = requests.post(
        url=f'{base_url}/subscription/subscribe/',
        json=dict(
            plan='platinum',
            payment_option='xyz',
            credit_card=dict(
                number='5586125903245963',
                expiry='2021/12',
                security_code='123'
            )
        ),
        headers=headers,
    )
    assert response.ok

    response = requests.get(url=f'{base_url}/content/silver/', headers=headers)
    assert response.ok

    response = requests.get(url=f'{base_url}/content/gold/', headers=headers)
    assert response.ok

    response = requests.get(url=f'{base_url}/content/platinum/', headers=headers)
    assert response.ok


def test_resubscribe():
    data = dict(
        username='silver.adams',
        password='password'
    )
    url = f'{base_url}/account/token/'
    response = requests.post(url, json=data)
    assert response.ok

    auth_key = response.json()['token']
    headers = dict(Authorization=f'Token {auth_key}')

    response = requests.get(f'{base_url}/subscription/ongoing/', headers=headers)
    assert response.ok

    response = requests.post(
        url=f'{base_url}/subscription/subscribe/',
        json=dict(
            plan='platinum',
            payment_option='xyz',
            credit_card=dict(
                number='5586125903245963',
                expiry='2021/12',
                security_code='123'
            )
        ),
        headers=headers,
    )
    assert not response.ok
    assert response.status_code == 400


def test_unsubscribe():
    data = dict(
        username='silver.adams',
        password='password'
    )
    url = f'{base_url}/account/token/'
    response = requests.post(url, json=data)
    assert response.ok

    auth_key = response.json()['token']
    headers = dict(Authorization=f'Token {auth_key}')

    response = requests.get(f'{base_url}/subscription/ongoing/', headers=headers)
    assert response.ok

    response = requests.post(
        url=f'{base_url}/subscription/unsubscribe/',
        json={'reason': 'hard to afford'},
        headers=headers
    )
    assert response.ok


def run():
    print('Make sure you have previously run setup!')
    test_silver_user()
    test_gold_user()
    test_platinum_user()
    test_resubscribe()
    test_unsubscribe()
