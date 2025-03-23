from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from api_requests import *
from btn_texts import *


def back_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_back)
    return keyb


def auth_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    sign_in = KeyboardButton(auth_texts.get('sign_in', {}).get(lang))
    sign_up = KeyboardButton(auth_texts.get('sign_up', {}).get(lang))
    keyb.add(sign_in, sign_up)
    return keyb


def language_btns():
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_ru = KeyboardButton("🇷🇺 Русский")
    btn_uz = KeyboardButton("🇺🇿 O'zbekcha")
    btn_en = KeyboardButton("🇺🇸 English")
    btn_de = KeyboardButton("🇩🇪 Deutsch")
    btn_hi = KeyboardButton("🇮🇳 भारतीय")
    keyb.add(btn_ru, btn_uz, btn_en)
    keyb.add(btn_de, btn_hi)
    return keyb


def city_btns(lang='ru', page=1):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    cities = get_cities(page)
    btns_list = []
    for item in cities['results']:
        btn = KeyboardButton(f"{item[f'name_{lang}']}")
        btns_list.append(btn)
        if len(btns_list) == 2:
            keyb.add(btns_list[0], btns_list[1])
            btns_list = []
    if len(btns_list) == 1:
        keyb.add(btns_list[0])

    btn_back = KeyboardButton(back_text.get(lang))
    previous_btn = KeyboardButton(f"{page - 1} {prev_text.get(lang)}")
    next_btn = KeyboardButton(f"{next_text.get(lang)} {page + 1}")
    if cities['previous'] and cities['next']:
        keyb.add(previous_btn, btn_back, next_btn)
    elif cities['previous'] and not cities['next']:
        keyb.add(previous_btn, btn_back)
    elif not cities['previous'] and cities['next']:
        keyb.add(btn_back, next_btn)
    else:
        keyb.add(btn_back)
    return keyb


def confirm_registration_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    confirm_btn = KeyboardButton(confirm_registration_text.get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(confirm_btn)
    keyb.add(btn_back)
    return keyb


def main_menu_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_exchange_currency = KeyboardButton(main_menu_texts['exchange_currency'].get(lang))
    btn_exchange_history = KeyboardButton(main_menu_texts['exchange_history'].get(lang))
    btn_withdraw = KeyboardButton(main_menu_texts['withdraw'].get(lang))
    send_btn = KeyboardButton(balance_section_texts.get('send', {}).get(lang))
    btn_subscription = KeyboardButton(main_menu_texts['subscription'].get(lang))
    btn_balance = KeyboardButton(main_menu_texts['balance'].get(lang))
    btn_reff_link = KeyboardButton(main_menu_texts['reff_link'].get(lang))
    btn_tex_work = KeyboardButton(main_menu_texts['tex_work'].get(lang))
    btn_settings = KeyboardButton(main_menu_texts['settings'].get(lang))
    keyb.add(btn_exchange_currency, btn_exchange_history)
    keyb.add(btn_withdraw, send_btn)
    keyb.add(btn_subscription, btn_balance)
    keyb.add(btn_reff_link, btn_tex_work)
    keyb.add(btn_settings)
    return keyb


def currency_type_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_fiat = KeyboardButton(currency_type_texts['fiat'].get(lang))
    btn_crypto = KeyboardButton(currency_type_texts['crypto'].get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_fiat, btn_crypto)
    keyb.add(btn_back)
    return keyb


def exchange_type_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_buy = KeyboardButton(exchange_type_texts['buy'].get(lang))
    btn_sell = KeyboardButton(exchange_type_texts['sell'].get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_buy, btn_sell)
    keyb.add(btn_back)
    return keyb


def currency_btns(lang='ru', page=1, filter_value=None, user_id=None, currency_type=None, status='simple'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    currencies = get_currencies(page, filter_value, user_id, currency_type, status)
    btns_list = []
    for item in currencies['results']:
        btn = KeyboardButton(f"{item['name']}")
        btns_list.append(btn)
        if len(btns_list) == 2:
            keyb.add(btns_list[0], btns_list[1])
            btns_list = []
    if len(btns_list) == 1:
        keyb.add(btns_list[0])

    btn_back = KeyboardButton(back_text.get(lang))
    previous_btn = KeyboardButton(f"{page - 1} {prev_text.get(lang)}")
    next_btn = KeyboardButton(f"{next_text.get(lang)} {page + 1}")
    if currencies['previous'] and currencies['next']:
        keyb.add(previous_btn, btn_back, next_btn)
    elif currencies['previous'] and not currencies['next']:
        keyb.add(previous_btn, btn_back)
    elif not currencies['previous'] and currencies['next']:
        keyb.add(btn_back, next_btn)
    else:
        keyb.add(btn_back)
    return keyb


def stock_btns(user_id, request_type='exchange', lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    if request_type == 'exchange':
        response = update_exchange(user_id=user_id, get_data='yes')
        btns_list = [
            KeyboardButton('{:7,.0f}'.format(item['amount']).replace(',', ' '))
            for item in response['currency_from']['stock_amounts']
        ]
    elif request_type == 'balance':
        response = update_balance(user_id=user_id, get_data='yes')
        btns_list = [
            KeyboardButton('{:7,.0f}'.format(item['amount']).replace(',', ' '))
            for item in response['currency']['stock_amounts']
        ]
    elif request_type == 'send':
        response = update_send(user_id=user_id, get_data='yes')
        btns_list = [
            KeyboardButton('{:7,.0f}'.format(item['amount']).replace(',', ' '))
            for item in response['currency']['stock_amounts']
        ]
    elif request_type == 'withdraw':
        response = update_withdraw(user_id=user_id, get_data='yes')
        btns_list = [
            KeyboardButton('{:7,.0f}'.format(item['amount']).replace(',', ' '))
            for item in response['currency']['stock_amounts']
        ]
    keyb.add(*btns_list)
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_back)
    return keyb


def balance_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_balance = KeyboardButton(balance_text.get(lang))
    btn_home = KeyboardButton(home_text.get(lang))
    keyb.add(btn_balance)
    keyb.add(btn_home)
    return keyb


def payment_type_btns(lang='ru', currency=None):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    if currency:
        providers = config.currency_providers.get(currency)
    else:
        providers = payment_type_texts
    btns_list = [
        KeyboardButton(item)
        for item in providers
    ]
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(*btns_list)
    keyb.add(btn_back)
    return keyb


def balance_section_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bonus_btn = KeyboardButton(balance_section_texts.get('bonus', {}).get(lang))
    fiat_btn = KeyboardButton(balance_section_texts.get('fiat', {}).get(lang))
    crypto_btn = KeyboardButton(balance_section_texts.get('crypto', {}).get(lang))
    reff_link_btn = KeyboardButton(balance_section_texts.get('reff_link', {}).get(lang))
    send_btn = KeyboardButton(balance_section_texts.get('send', {}).get(lang))
    hash_btn = KeyboardButton(balance_section_texts.get('hash', {}).get(lang))
    btn_home = KeyboardButton(home_text.get(lang))
    # keyb.add(bonus_btn)
    keyb.add(fiat_btn, crypto_btn)
    keyb.add(reff_link_btn, send_btn)
    keyb.add(hash_btn)
    keyb.add(btn_home)
    return keyb


def balance_action_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    fill_btn = KeyboardButton(balance_action_texts.get('fill', {}).get(lang))
    convert_btn = KeyboardButton(balance_action_texts.get('convert', {}).get(lang))
    btn_home = KeyboardButton(home_text.get(lang))
    keyb.add(fill_btn, convert_btn)
    keyb.add(btn_home)
    return keyb


def balance_bill_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    payed_btn = KeyboardButton(balance_bill_texts.get('payed', {}).get(lang))
    cancel_btn = KeyboardButton(balance_bill_texts.get('cancel', {}).get(lang))
    keyb.add(payed_btn, cancel_btn)
    return keyb


def accept_balance_btns(lang='ru', user_id='', balance_id=''):
    keyb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(confirmation_texts.get('confirm', {}).get(lang), callback_data=f"confirm_balance_{user_id}_{balance_id}")
    btn_deny = InlineKeyboardButton(confirmation_texts.get('deny', {}).get(lang), callback_data=f"deny_balance_{user_id}_{balance_id}")
    keyb.add(btn_accept, btn_deny)
    return keyb


def settings_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_cabinet = KeyboardButton(settings_texts['cabinet'].get(lang))
    btn_change_language = KeyboardButton(settings_texts['change_language'].get(lang))
    btn_change_country = KeyboardButton(settings_texts['change_country'].get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_cabinet, btn_change_language)
    keyb.add(btn_change_country)
    keyb.add(btn_back)
    return keyb


def cabinet_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_username = KeyboardButton(cabinet_texts['username'].get(lang))
    btn_password = KeyboardButton(cabinet_texts['password'].get(lang))
    btn_logout = KeyboardButton(cabinet_texts['logout'].get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_username, btn_password)
    keyb.add(btn_logout)
    keyb.add(btn_back)
    return keyb


def profile_btns(lang='ru'):
    keyb = InlineKeyboardMarkup()
    btn_link = InlineKeyboardButton(profile_text.get(lang), url=f"{config.site_url}/settings-profile/")
    keyb.add(btn_link)
    return keyb


def tex_work_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    tex_works = get_tex_works()
    for item in tex_works:
        btn_tex_work = KeyboardButton(item[f"name_{lang}"])
        keyb.add(btn_tex_work)
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_back)
    return keyb


def subscription_menu_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_advantages = KeyboardButton(subscription_menu_texts.get('advantages', {}).get(lang))
    btn_check_subscription = KeyboardButton(subscription_menu_texts.get('check_subscription', {}).get(lang))
    btn_new_subscription = KeyboardButton(subscription_menu_texts.get('new_subscription', {}).get(lang))
    btn_reff_link = KeyboardButton(subscription_menu_texts.get('reff_link', {}).get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_advantages, btn_check_subscription)
    keyb.add(btn_new_subscription, btn_reff_link)
    keyb.add(btn_back)
    return keyb


def subscription_update_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_update_subscription = KeyboardButton(subscription_update_texts.get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_update_subscription)
    keyb.add(btn_back)
    return keyb


def subscription_new_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_new_subscription = KeyboardButton(subscription_menu_texts.get('new_subscription', {}).get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_new_subscription)
    keyb.add(btn_back)
    return keyb


def discount_format(discount):
    if discount != 0:
        return f" (-{discount}%)"
    else:
        return ""


def subscription_period_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn_list = [
        KeyboardButton(f"{item[f'name_{lang}']}{discount_format(item['discount'])}")
        for item in get_subscription_periods()
    ]
    keyb.add(*btn_list)
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_back)
    return keyb


def subscription_type_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn_list = [
        KeyboardButton(f"Oval {item[f'name'].capitalize()} 💎")
        for item in get_subscription_types()
    ]
    keyb.add(*btn_list)
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_back)
    return keyb


def confirmation_btns(lang='ru'):
    keyb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_confirm = KeyboardButton(confirmation_texts.get('confirm', {}).get(lang))
    btn_deny = KeyboardButton(confirmation_texts.get('deny', {}).get(lang))
    btn_back = KeyboardButton(back_text.get(lang))
    keyb.add(btn_confirm, btn_deny)
    keyb.add(btn_back)
    return keyb


def accept_withdraw_btns(lang='ru', user_id='', withdraw_id=''):
    keyb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(confirmation_texts.get('confirm', {}).get(lang), callback_data=f"confirm_withdraw_{user_id}_{withdraw_id}")
    btn_deny = InlineKeyboardButton(confirmation_texts.get('deny', {}).get(lang), callback_data=f"deny_withdraw_{user_id}_{withdraw_id}")
    keyb.add(btn_accept, btn_deny)
    return keyb


def accept_send_btns(lang='ru', user_id='', send_id=''):
    keyb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(confirmation_texts.get('confirm', {}).get(lang), callback_data=f"confirm_send_{user_id}_{send_id}")
    btn_deny = InlineKeyboardButton(confirmation_texts.get('deny', {}).get(lang), callback_data=f"deny_send_{user_id}_{send_id}")
    keyb.add(btn_accept, btn_deny)
    return keyb


def accepted_btns(lang='ru'):
    keyb = InlineKeyboardMarkup()
    btn_accepted = InlineKeyboardButton(accepted_text.get(lang), callback_data=f"already_accepted")
    keyb.add(btn_accepted)
    return keyb


def denied_btns(lang='ru'):
    keyb = InlineKeyboardMarkup()
    btn_denied = InlineKeyboardButton(denied_text.get(lang), callback_data=f"already_denied")
    keyb.add(btn_denied)
    return keyb


def choose_currency_option_btns(lang='ru', exchange_id=None):
    keyb = InlineKeyboardMarkup()
    rates = get_available_exchange_rates(exchange_id=exchange_id)
    for item in rates:
        btn = InlineKeyboardButton(item['rate'], callback_data=f"exchange_rate_{exchange_id}_{item['slug_value']}")
        if item['type'] == 'template':
            btn = InlineKeyboardButton(item['rate'], callback_data=f"exchange_rate_{exchange_id}_{item['slug_value']}")
        keyb.add(btn)
    return keyb
