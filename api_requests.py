import requests
import json
from telebot.types import Message
import config


def load_company_data():
    response = requests.get(f'{config.site_url}/api/about/view/')
    json_data = json.loads(response.text)[0]
    return json_data


def update_user(**kwargs):
    try:
        url = f"{config.site_url}/api/trader/create-user/"
        response = requests.post(url=url, data=kwargs)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_trader_data(user_id):
    try:
        url = f"{config.site_url}/api/trader/info/?user_id={user_id}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_user_lang(user_id):
    try:
        url = f"{config.site_url}/api/trader/get-lang/"
        response = requests.post(url=url, data={'user_id': user_id})
        json_data = json.loads(response.text)
        if 'lang' in json_data and json_data['lang'] != 'empty':
            return json_data['lang']
        return 'empty'
    except Exception as e:
        print(e)
        return 'empty'


def get_cities(page):
    try:
        url = f"{config.site_url}/api/city/view/?type=get_for_bot&page={page}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_city_by_name(name):
    try:
        url = f"{config.site_url}/api/city/view/?type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def check_username(username, user_id):
    try:
        url = f"{config.site_url}/api/trader/check-username/"
        response = requests.post(url=url, data={'username': username, 'user_id': user_id})
        json_data = json.loads(response.text)
        return json_data['username_valid']
    except Exception as e:
        print(e)


def check_password(username, password):
    try:
        url = f"{config.site_url}/api/trader/check-password/"
        response = requests.post(url=url, data={'username': username, 'password': password})
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_currencies(page, filter_value=None, user_id=None, currency_type=None, status='simple'):
    try:
        url = f"{config.site_url}/api/currency/view/?page={page}"
        if filter_value and user_id:
            url += f"&filter_value={filter_value}&user_id={user_id}"
        if currency_type:
            url += f"&currency_type={currency_type}"
        if status:
            url += f"&status={status}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_currency_by_name(name):
    try:
        url = f"{config.site_url}/api/currency/view/?type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def update_exchange(**kwargs):
    try:
        url = f"{config.site_url}/api/exchange/update/"
        response = requests.post(url=url, data=kwargs)
        if kwargs.get('get_data'):
            json_data = json.loads(response.text)
            return json_data['exchange']
    except Exception as e:
        print(e)


def user_exchanges(user_id, currency_type=None):
    try:
        url = f"{config.site_url}/api/exchange/view/?type=get_by_user_id&user_id={user_id}"
        if currency_type is not None:
            url += f"&currency_type={currency_type}"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_available_exchange_rates(**kwargs):
    try:
        url = f"{config.site_url}/api/exchange/rates/"
        response = requests.post(url, data=kwargs)
        json_data = json.loads(response.text)
        return json_data['rates']
    except Exception as e:
        print(e)


def update_balance(**kwargs):
    try:
        url = f"{config.site_url}/api/balance/update/"
        response = requests.post(url=url, data=kwargs)
        if kwargs.get('get_data'):
            json_data = json.loads(response.text)
            return json_data['balance']
    except Exception as e:
        print(e)


def check_balance_for_bonus(user_id):
    try:
        url = f"{config.site_url}/api/balance/check/?user_id={user_id}&type=bonus"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['balance']
    except Exception as e:
        print(e)


def check_balance_for_exchange(user_id):
    try:
        url = f"{config.site_url}/api/balance/check/?user_id={user_id}&type=exchange"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['balance']
    except Exception as e:
        print(e)


def check_balance_for_withdraw(user_id):
    try:
        url = f"{config.site_url}/api/balance/check/?user_id={user_id}&type=withdraw"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['balance']
    except Exception as e:
        print(e)


def user_has_balance(user_id):
    try:
        url = f"{config.site_url}/api/balance/has/?user_id={user_id}"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['result']
    except Exception as e:
        print(e)


def get_all_balances(user_id, currency_type='all'):
    try:
        url = f"{config.site_url}/api/balance/get_all/?user_id={user_id}&currency_type={currency_type}"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['balances']
    except Exception as e:
        print(e)


def update_send(**kwargs):
    try:
        url = f"{config.site_url}/api/send/update/"
        response = requests.post(url=url, data=kwargs)
        if kwargs.get('get_data'):
            json_data = json.loads(response.text)
            return json_data['send']
        elif kwargs.get('get_all'):
            json_data = json.loads(response.text)
            return json_data
    except Exception as e:
        print(e)


def check_balance_for_send(user_id):
    try:
        url = f"{config.site_url}/api/balance/check/?user_id={user_id}&type=send"
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['balance']
    except Exception as e:
        print(e)


def check_hash(hash_code):
    try:
        url = f"{config.site_url}/api/trader/check-hash/?hash={hash_code}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data['result']
    except Exception as e:
        print(e)


def update_withdraw(**kwargs):
    try:
        url = f"{config.site_url}/api/withdraw/update/"
        response = requests.post(url=url, data=kwargs)
        if kwargs.get('get_data'):
            json_data = json.loads(response.text)
            return json_data['withdraw']
    except Exception as e:
        print(e)


def get_tex_works(name=None):
    try:
        url = f"{config.site_url}/api/tex_work/view/"
        if name is not None:
            url += f"?type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def update_subscription(**kwargs):
    try:
        url = f"{config.site_url}/api/subscription/update/"
        response = requests.post(url=url, data=kwargs)
        if kwargs.get('get_data'):
            json_data = json.loads(response.text)
            return json_data['subscription']
    except Exception as e:
        print(e)


def get_subscription_types(name=None, status='active'):
    try:
        url = f"{config.site_url}/api/subscription_type/view/?status={status}"
        if name is not None:
            url += f"&type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_subscription_periods(name=None):
    try:
        url = f"{config.site_url}/api/subscription_period/view/"
        if name is not None:
            url += f"?type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_subscription_permissions(**kwargs):
    try:
        url = f"{config.site_url}/api/subscription/permissions/"
        response = requests.post(url=url, data=kwargs)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def get_explanations(name=None):
    try:
        url = f"{config.site_url}/api/explanation/view/"
        if name is not None:
            url += f"?type=get_by_name&name={name}"
        response = requests.get(url=url)
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print(e)


def logout_user(user_id):
    try:
        url = f"{config.site_url}/api/trader/logout/"
        requests.post(url=url, data={'user_id': user_id})
    except Exception as e:
        print(e)
