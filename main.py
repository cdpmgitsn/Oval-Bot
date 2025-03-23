import telebot
from telebot import types
from telebot.types import LabeledPrice

import config
import messages
from btns import *
from api_requests import *
from utils import *


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    try:
        chat_id = message.chat.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        lang_code = message.from_user.language_code
        lang = get_user_lang(chat_id)
        if lang == 'empty':
            trader_id = None
            exchange_id = None
            splitted_text = message.text.split('/start ')
            if len(splitted_text) > 1:
                for item in splitted_text:
                    if item.startswith('trader_'):
                        trader_id = item.replace('trader_', '')
                    elif item.startswith('exchange_'):
                        exchange_id = item.replace('exchange_', '')
            update_user(user_id=chat_id, username=username, first_name=first_name, last_name=last_name, chat_id=chat_id, lang_code=lang_code, trader_id=trader_id, exchange_id=exchange_id)
            msg = messages.language_msg
            keyb = language_btns()
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_language)
        else:
            user_data = update_user(user_id=chat_id, username=username, first_name=first_name, last_name=last_name)
            if user_data.get('trader') == f"{chat_id}":
                msg = messages.get_username_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_username)
            else:
                msg = messages.main_menu_msg.get(lang)
                keyb = main_menu_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


def get_language(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        if text in ["🇷🇺 Русский", "🇺🇿 O'zbekcha", "🇺🇸 English", "🇩🇪 Deutsch", "🇮🇳 भारतीय"]:
            if text == "🇷🇺 Русский":
                lang = 'ru'
            elif text == "🇺🇿 O'zbekcha":
                lang = 'uz'
            elif text == "🇺🇸 English":
                lang = 'en'
            elif text == "🇩🇪 Deutsch":
                lang = 'de'
            elif text == "🇮🇳 भारतीय":
                lang = 'hi'

            user_data = update_user(user_id=chat_id, lang_code=lang)
            if user_data.get('city')[f'name_{lang}'] == '':
                msg = messages.get_city_msg.get(lang)
                keyb = city_btns(lang, page=1)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_city)
            else:
                msg = messages.main_menu_msg.get(lang)
                keyb = main_menu_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
        else:
            msg = messages.language_msg
            keyb = language_btns()
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_language)
    except Exception as e:
        print(e)


def get_city(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.settings_msg.get(lang)
            keyb = settings_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_settings_menu)
        elif text.endswith(prev_text.get(lang)):
            page = text.split(' ')[0]
            msg = messages.get_city_msg.get(lang)
            keyb = city_btns(lang, page=int(page))
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_city)
        elif text.startswith(next_text.get(lang)):
            page = text.split(' ')[-1]
            msg = messages.get_city_msg.get(lang)
            keyb = city_btns(lang, page=int(page))
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_city)
        elif text == "🚫":
            msg = messages.no_city_msg.get(lang)
            bot.reply_to(message, msg)
            bot.register_next_step_handler(message, get_city)
        else:
            city = get_city_by_name(text)
            if city['count'] == 0:
                msg = messages.no_city_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_city)
            else:
                city_id = city['results'][0]['id']
                user_data = update_user(user_id=chat_id, city_id=city_id)
                if user_data.get('trader') == f"{chat_id}":
                    msg = messages.get_username_msg.get(lang)
                    keyb = back_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_username)
                else:
                    msg = messages.settings_msg.get(lang)
                    keyb = settings_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_settings_menu)
    except Exception as e:
        print(e)


def get_username(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if message.content_type == 'text':
            if text == back_text.get(lang):
                msg = messages.get_city_msg.get(lang)
                keyb = city_btns(lang, page=1)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_city)
            else:
                username_valid = check_username(text, chat_id)
                if username_valid == 'yes':
                    user = update_user(user_id=chat_id, trader_username=text)
                    if user['password']:
                        msg = messages.main_menu_msg.get(lang)
                        keyb = main_menu_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                    else:
                        msg = messages.get_password_msg.get(lang)
                        keyb = back_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, get_password)
                else:
                    msg = messages.wrong_username_msg.get(lang)
                    keyb = back_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_username)
        else:
            msg = messages.get_username_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_username)
    except Exception as e:
        print(e)


def get_password(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if message.content_type == 'text':
            if text == back_text.get(lang):
                update_user(user_id=chat_id, trader_username=chat_id)
                msg = messages.get_username_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_username)
            else:
                user = update_user(user_id=chat_id, password=text)
                if user['registration_finished']:
                    msg = messages.main_menu_msg.get(lang)
                    keyb = main_menu_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                else:
                    msg = messages.confirm_registration_msg.get(lang)
                    keyb = confirm_registration_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, confirm_registration)
        else:
            msg = messages.get_password_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_password)
    except Exception as e:
        print(e)


def confirm_registration(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.get_password_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_password)
        elif text == confirm_registration_text.get(lang):
            update_user(user_id=chat_id, registration_finished='yes')
            msg = messages.confirmed_registration_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.confirm_registration_msg.get(lang)
            keyb = confirm_registration_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, confirm_registration)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def get_section(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == main_menu_texts.get('exchange_currency', {}).get(lang):
            permissions = get_subscription_permissions(user_id=chat_id)
            if permissions['exchange']:
                msg = messages.currency_type_msg.get(lang)
                keyb = currency_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_currency_type)
            else:
                msg = messages.exchange_limit_msg.get(lang)
                keyb = main_menu_btns(lang)
                bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == main_menu_texts.get('exchange_history', {}).get(lang):
            msg = messages.history_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_history_currency_type)
        elif text == main_menu_texts.get('withdraw', {}).get(lang):
            permissions = get_subscription_permissions(user_id=chat_id)
            if permissions['exchange']:
                msg = messages.currency_type_msg.get(lang)
                keyb = currency_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_currency_type)
            else:
                msg = messages.withdraw_limit_msg.get(lang)
                keyb = main_menu_btns(lang)
                bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == balance_section_texts.get('send', {}).get(lang):
            permissions = get_subscription_permissions(user_id=chat_id)
            if permissions['send']:
                msg = messages.currency_type_msg.get(lang)
                keyb = currency_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_send_currency_type)
            else:
                msg = messages.send_limit_msg.get(lang)
                keyb = balance_section_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_balance_section)
        elif text == main_menu_texts.get('subscription', {}).get(lang):
            msg = messages.subscription_menu_msg.get(lang)
            keyb = subscription_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, subscription_menu)
        elif text == main_menu_texts.get('balance', {}).get(lang):
            msg = messages.get_section_msg.get(lang)
            keyb = balance_section_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_section)
        elif text == main_menu_texts.get('reff_link', {}).get(lang):
            explanation = get_explanations('reff_link')
            msg = explanation[0][f'description_{lang}']
            msg = "\n".join(msg.split('<br>'))
            bot.send_message(chat_id, msg, parse_mode='html')

            user_data = get_trader_data(user_id=chat_id)
            msg = messages.reff_link_msg.get(lang)
            msg += "\n\n"
            msg += f"{config.site_url}/reff_link/{user_data['hash']}/"
            bot.send_message(chat_id, msg)
        elif text == main_menu_texts.get('tex_work', {}).get(lang):
            msg = messages.tex_work_msg.get(lang)
            keyb = tex_work_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_tex_work)
        elif text == main_menu_texts.get('settings', {}).get(lang):
            msg = messages.settings_msg.get(lang)
            keyb = settings_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_settings_menu)
        else:
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_currency_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [currency_type_texts.get('fiat', {}).get(lang), currency_type_texts.get('crypto', {}).get(lang)]:
            currency_type = 'fiat'
            if currency_type_texts.get('crypto', {}).get(lang) == text:
                currency_type = 'crypto'
            update_exchange(user_id=chat_id, currency_type=currency_type, new='yes')
            msg = messages.exchange_type_msg.get(lang)
            keyb = exchange_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_type)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_type)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [exchange_type_texts.get('buy', {}).get(lang), exchange_type_texts.get('sell', {}).get(lang)]:
            exchange_type = 'buy'
            if text == exchange_type_texts.get('sell', {}).get(lang):
                exchange_type = 'sell'
            update_exchange(user_id=chat_id, exchange_type=exchange_type)
            msg = messages.exchange_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, filter_value='currency_from', user_id=chat_id, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_from)
        elif text == back_text.get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_type)
        else:
            msg = messages.exchange_type_msg.get(lang)
            keyb = exchange_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_type)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_currency_from(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.exchange_type_msg.get(lang)
            keyb = exchange_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_type)
        elif text.endswith(prev_text.get(lang)):
            page = text.split(' ')[0]
            msg = messages.exchange_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), filter_value='currency_from', user_id=chat_id, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_from)
        elif text.startswith(next_text.get(lang)):
            page = text.split(' ')[-1]
            msg = messages.exchange_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), filter_value='currency_from', user_id=chat_id, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_from)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_exchange_currency_from)
            else:
                currency_id = currency['results'][0]['id']
                exchange = update_exchange(user_id=chat_id, currency_from_id=currency_id, get_data='yes')
                if exchange['currency_type'] == 'crypto':
                    msg = messages.exchange_currency_msg.get(lang)
                    subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                    keyb = currency_btns(lang, filter_value='currency_to', user_id=chat_id, status=subscription)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_exchange_currency_to)
                else:
                    msg = messages.exchange_input_msg.get(lang)
                    keyb = stock_btns(chat_id, 'exchange', lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_exchange_input)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_input(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            exchange = update_exchange(user_id=chat_id, get_data='yes')
            if exchange['currency_type'] == 'crypto':
                msg = messages.exchange_currency_msg.get(lang)
                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                keyb = currency_btns(lang, filter_value='currency_to', user_id=chat_id, status=subscription)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_currency_to)
            else:
                msg = messages.exchange_currency_msg.get(lang)
                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                keyb = currency_btns(lang, filter_value='currency_from', user_id=chat_id, status=subscription)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_currency_from)
        else:
            amount_input = text.replace(' ', '')
            if amount_input.isdigit():
                exchange = update_exchange(user_id=chat_id, get_data='yes')
                
                permissions = get_subscription_permissions(user_id=chat_id)
                if not (exchange['currency_type'] == 'fiat' and exchange['exchange_type'] == 'buy'):
                    amount_input = float(amount_input) * permissions['exchange_fee']
                
                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                limit = exchange['currency_from'][f"{subscription}_max_price"]
                
                if float(amount_input) <= limit:
                    if exchange['exchange_type'] == 'buy':
                        if exchange['currency_type'] == 'crypto':
                            balance = check_balance_for_exchange(user_id=chat_id)
                            if balance > exchange['amount_output']:
                                exchange = update_exchange(user_id=chat_id, amount_input=amount_input, fees=permissions['exchange_fee'], get_data='yes')
                                msg = messages.exchange_choose_msg.get(lang)
                                keyb = choose_currency_option_btns(lang, exchange['id'])
                                bot.send_message(chat_id, msg, reply_markup=keyb)
                            else:
                                msg = messages.no_balance_msg.get(lang)
                                keyb = balance_btns(lang)
                                bot.reply_to(message, msg, reply_markup=keyb)
                                bot.register_next_step_handler(message, balance_menu)
                        else:
                            exchange = update_exchange(user_id=chat_id, amount_input=amount_input, fees=permissions['exchange_fee'], get_data='yes')
                            msg = messages.exchange_currency_msg.get(lang)
                            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                            keyb = currency_btns(lang, filter_value='currency_to', user_id=chat_id, status=subscription)
                            bot.reply_to(message, msg, reply_markup=keyb)
                            bot.register_next_step_handler(message, get_exchange_currency_to)
                    else:
                        balance = check_balance_for_exchange(user_id=chat_id)
                        if balance > float(amount_input):
                            update_exchange(user_id=chat_id, amount_input=amount_input, fees=permissions['exchange_fee'])
                            exchange = update_exchange(user_id=chat_id, get_data='yes')
                            if exchange['currency_type'] == 'crypto':
                                msg = messages.exchange_choose_msg.get(lang)
                                keyb = choose_currency_option_btns(lang, exchange['id'])
                                bot.send_message(chat_id, msg, reply_markup=keyb)
                            else:
                                msg = messages.exchange_currency_msg.get(lang)
                                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                                keyb = currency_btns(lang, filter_value='currency_to', user_id=chat_id, status=subscription)
                                bot.reply_to(message, msg, reply_markup=keyb)
                                bot.register_next_step_handler(message, get_exchange_currency_to)
                        else:
                            msg = messages.no_balance_msg.get(lang)
                            keyb = balance_btns(lang)
                            bot.reply_to(message, msg, reply_markup=keyb)
                            bot.register_next_step_handler(message, balance_menu)
                else:
                    msg = messages.exchange_limit_msg.get(lang)
                    keyb = stock_btns(chat_id, 'exchange', lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_exchange_input)
            else:
                msg = messages.exchange_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'exchange', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_input)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_currency_to(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            exchange = update_exchange(user_id=chat_id, get_data='yes')
            if exchange['currency_type'] == 'crypto':
                msg = messages.exchange_currency_msg.get(lang)
                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                keyb = currency_btns(lang, filter_value='currency_from', user_id=chat_id, status=subscription)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_currency_from)
            else:
                msg = messages.exchange_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'exchange', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_input)
        elif text.endswith(prev_text.get(lang)):
            page = text.split(' ')[0]
            msg = messages.exchange_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), filter_value='currency_to', user_id=chat_id, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_to)
        elif text.startswith(next_text.get(lang)):
            page = text.split(' ')[-1]
            msg = messages.exchange_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), filter_value='currency_to', user_id=chat_id, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_currency_to)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_exchange_currency_to)
            else:
                currency_id = currency['results'][0]['id']
                exchange = update_exchange(user_id=chat_id, currency_to_id=currency_id, get_data='yes')
                if exchange['exchange_type'] == 'buy':
                    balance = check_balance_for_exchange(user_id=chat_id)
                    if balance > exchange['amount_output']:
                        if exchange['currency_type'] == 'crypto':
                            msg = messages.exchange_input_msg.get(lang)
                            keyb = stock_btns(chat_id, 'exchange', lang)
                            bot.reply_to(message, msg, reply_markup=keyb)
                            bot.register_next_step_handler(message, get_exchange_input)
                        else:
                            msg = messages.exchange_choose_msg.get(lang)
                            keyb = choose_currency_option_btns(lang, exchange['id'])
                            bot.send_message(chat_id, msg, reply_markup=keyb)
                    else:
                        msg = messages.no_balance_msg.get(lang)
                        keyb = balance_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, balance_menu)
                else:
                    if exchange['currency_type'] == 'crypto':
                        msg = messages.exchange_input_msg.get(lang)
                        keyb = stock_btns(chat_id, 'exchange', lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, get_exchange_input)
                    else:
                        msg = messages.exchange_choose_msg.get(lang)
                        keyb = choose_currency_option_btns(lang, exchange['id'])
                        bot.send_message(chat_id, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#! Exchange
def get_exchange_wallet(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.exchange_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'exchange', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_exchange_input)
        else:
            exchange = update_exchange(user_id=chat_id, wallet=text, get_data='yes')
            msg = messages.exchange_choose_msg.get(lang)
            keyb = choose_currency_option_btns(lang, exchange['id'])
            bot.send_message(chat_id, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#! Exchange
def confirm_exchange(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            exchange = update_exchange(user_id=chat_id, get_data='yes')
            msg = messages.exchange_choose_msg.get(lang)
            keyb = choose_currency_option_btns(lang, exchange['id'])
            bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == confirmation_texts.get('confirm', {}).get(lang):
            exchange = update_exchange(user_id=chat_id, confirmed='yes', get_data='yes')
            msg = messages.exchange_accepted_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == confirmation_texts.get('deny', {}).get(lang):
            msg = messages.exchange_denied_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#? Balance 
def get_balance_section(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == balance_section_texts.get('bonus', {}).get(lang):
            balance = check_balance_for_bonus(user_id=chat_id)
            if balance > 0:
                pass
        elif text in [balance_section_texts.get('fiat', {}).get(lang), balance_section_texts.get('crypto', {}).get(lang)]:
            msg = messages.balance_result_msg.get(lang)
            currency_type = 'fiat'
            if text == balance_section_texts.get('crypto', {}).get(lang):
                currency_type = 'crypto'
            balances = get_all_balances(chat_id, currency_type)
            for item in balances:
                current_balance = 0
                if item['balance'] != None:
                    current_balance = item['balance']
                    if current_balance > 1:
                        if are_decimal_digits_zero(current_balance):
                            current_balance = '{:7,.0f}'.format(current_balance).replace(' ', '')
                        else:
                            current_balance = '{:7,.2f}'.format(current_balance).replace(' ', '')
                msg += f"\n{item['currency']} = {current_balance} {item['symbol']}"
            keyb = balance_action_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_action)
        elif text == balance_section_texts.get('reff_link', {}).get(lang):
            explanation = get_explanations('reff_link')
            msg = explanation[0][f'description_{lang}']
            msg = "\n".join(msg.split('<br>'))
            bot.send_message(chat_id, msg, parse_mode='html')

            user_data = get_trader_data(user_id=chat_id)
            msg = messages.reff_link_msg.get(lang)
            msg += "\n\n"
            msg += f"{config.site_url}/reff_link/{user_data['hash']}/"
            bot.send_message(chat_id, msg)
        elif text == balance_section_texts.get('send', {}).get(lang):
            permissions = get_subscription_permissions(user_id=chat_id)
            if permissions['send']:
                msg = messages.currency_type_msg.get(lang)
                keyb = currency_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_send_currency_type)
            else:
                msg = messages.send_limit_msg.get(lang)
                keyb = balance_section_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_balance_section)
        elif text == balance_section_texts.get('hash', {}).get(lang):
            explanation = get_explanations('hash')
            msg = explanation[0][f'description_{lang}']
            msg = "\n".join(msg.split('<br>'))
            bot.send_message(chat_id, msg, parse_mode='html')

            hash_code = get_trader_data(user_id=chat_id)['hash']
            msg = f"`{hash_code}`"
            keyb = balance_section_btns(lang)
            bot.reply_to(message, msg, parse_mode='Markdown')
            bot.register_next_step_handler(message, get_balance_section)
        else:
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#? Balance 
def get_balance_action(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == balance_action_texts.get('fill', {}).get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency_type)
        elif text == balance_action_texts.get('convert', {}).get(lang):
            permissions = get_subscription_permissions(user_id=chat_id)
            if permissions['exchange']:
                msg = messages.currency_type_msg.get(lang)
                keyb = currency_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_exchange_currency_type)
            else:
                msg = messages.exchange_limit_msg.get(lang)
                keyb = balance_action_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_balance_action)
        else:
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#? Balance
def balance_menu(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == balance_text.get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency_type)
        elif text == home_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.no_balance_msg.get(lang)
            keyb = balance_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, balance_menu)
    except Exception as e:
        print(e)


#? Balance
def get_balance_currency_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [currency_type_texts.get('fiat', {}).get(lang), currency_type_texts.get('crypto', {}).get(lang)]:
            currency_type = 'fiat'
            if currency_type_texts.get('crypto', {}).get(lang) == text:
                currency_type = 'crypto'
            update_balance(user_id=chat_id, currency_type=currency_type, get_data='yes')
            msg = messages.balance_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type=currency_type, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency_type)
    except Exception as e:
        print(e)


#? Balance
def get_balance_currency(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency_type)
        elif text.endswith(prev_text.get(lang)):
            balance = update_balance(user_id=chat_id, get_data='yes')
            page = text.split(' ')[0]
            msg = messages.balance_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=balance['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency)
        elif text.startswith(next_text.get(lang)):
            balance = update_balance(user_id=chat_id, get_data='yes')
            page = text.split(' ')[-1]
            msg = messages.balance_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=balance['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_balance_currency)
            else:
                currency_id = currency['results'][0]['id']
                update_balance(user_id=chat_id, update_type='plus', currency_id=currency_id)
                msg = messages.balance_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'balance', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_balance_input)
    except Exception as e:
        print(e)


#? Balance
def get_balance_input(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.balance_currency_msg.get(lang)
            balance = update_balance(user_id=chat_id, get_data='yes')
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type=balance['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_currency)
        else:
            amount_input = text.replace(' ', '')
            if amount_input.isdigit():
                balance = update_balance(user_id=chat_id, amount=amount_input, get_data='yes')
                msg = "Время обработки вашей заявки  ➡️  от 15 до 45 ⬅️ минут  ⌛️\n"
                msg += f"\n"
                msg += f"#️⃣ Номер заявки: {balance['id']}\n"
                msg += f"📎 ID пользователья: {chat_id}\n"
                msg += f"💵 Валюта пополнения: {balance['currency']['name']}\n"
                msg += f"🔢 Сумма пополнения: {balance['amount']} {balance['currency']['name']}\n"
                msg += f"\n"
                msg += f"🔹🔹🔹🔹🔹🔹\n"
                msg += f"\n"
                msg += f"Этапы действий: \n"
                msg += f"\n"
                if balance['currency_type'] == 'crypto':
                    msg += f"1. Произведите копирование следующего кошелька: `{balance['currency']['wallet']}`.\n"
                else:
                    msg += f"1. Произведите копирование следующей карты: `{balance['currency']['wallet']}` {balance['currency']['holder']}.\n"
                msg += f"\n"
                msg += f"2. Осуществите перевод средств в соответствии с ранее предоставленным запросом.\n"
                msg += f"\n"
                msg += f"3. По завершении перевода, пожалуйста, нажмите на кнопку \"Оплатил ✅\".\n"
                msg += f"\n"
                msg += f"\n"
                msg += f"❗️При возникновении затруднений или непонимания, необходимо обратиться к оператору для получения поддержки.\n"
                msg += f"\n"
                msg += f"📍Тех.поддержка 👨‍💻@ovalsupport\\_bot\n"
                keyb = balance_bill_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb, parse_mode='Markdown')
                bot.register_next_step_handler(message, confirm_balance)

                #! For fiat
                # msg = messages.balance_payment_type_msg.get(lang)
                # keyb = payment_type_btns(lang)
                # bot.reply_to(message, msg, reply_markup=keyb)
                # bot.register_next_step_handler(message, get_balance_payment_type)
            else:
                msg = messages.balance_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'balance', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_balance_input)
    except Exception as e:
        print(e)


#? Balance
def confirm_balance(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.balance_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'balance', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_input)
        elif text == balance_bill_texts.get('payed', {}).get(lang):
            balance = update_balance(user_id=chat_id, confirmed='yes', get_data='yes')

            # To Group
            msg = f"#️⃣ Номер заявки: {balance['id']}\n"
            msg += f"📎 ID пользователья: {chat_id}\n"
            msg += f"💵 Валюта пополнения: {balance['currency']['name']}\n"
            msg += f"🔢 Сумма пополнения: {balance['amount']} {balance['currency']['name']}\n"
            keyb = accept_balance_btns(lang, user_id=chat_id, balance_id=balance['id'])
            bot.send_message(config.balance_group_id[balance['currency_type']], msg, reply_markup=keyb)

            # To User
            msg = messages.balance_confirmed_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == balance_bill_texts.get('cancel', {}).get(lang):
            msg = messages.balance_canceled_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
        else:
            balance = update_balance(user_id=chat_id, get_data='yes')
            msg = "Время обработки вашей заявки  ➡️  от 15 до 45 ⬅️ минут  ⌛️\n"
            msg += f"\n"
            msg += f"#️⃣ Номер заявки: {balance['id']}\n"
            msg += f"📎 ID пользователья: {chat_id}\n"
            msg += f"💵 Валюта пополнения: {balance['currency']['name']}\n"
            msg += f"🔢 Сумма пополнения: {balance['amount']} {balance['currency']['name']}\n"
            msg += f"\n"
            msg += f"🔹🔹🔹🔹🔹🔹\n"
            msg += f"\n"
            msg += f"Этапы действий: \n"
            msg += f"\n"
            msg += f"1. Произведите копирование следующего кошелька: `{balance['currency']['wallet']}`.\n"
            msg += f"\n"
            msg += f"2. Осуществите перевод средств в соответствии с ранее предоставленным запросом.\n"
            msg += f"\n"
            msg += f"3. По завершении перевода, пожалуйста, нажмите на кнопку \"Оплатил ✅\".\n"
            msg += f"\n"
            msg += f"\n"
            msg += f"❗️При возникновении затруднений или непонимания, необходимо обратиться к оператору для получения поддержки.\n"
            msg += f"\n"
            msg += f"📍Тех.поддержка 👨‍💻@ovalsupport\\_bot\n"
            keyb = balance_bill_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb, parse_mode='Markdown')
            bot.register_next_step_handler(message, confirm_balance)
    except Exception as e:
        print(e)


#? Balance
def get_balance_payment_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.balance_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'balance', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_input)
        elif text in payment_type_texts:
            last_balance = update_balance(user_id=chat_id, payment_type=text, get_data='yes')
            company_data = load_company_data()

            prices = [
                LabeledPrice(label=messages.balance_invoice_msg.get(lang), amount=int(last_balance['amount'])*100),
            ]

            bot.send_invoice(
                chat_id=message.chat.id,  # chat_id
                title=f"{company_data['name']}",  # title
                description=messages.balance_invoice_description_msg.get(lang),  # description
                invoice_payload=f"balance_{last_balance['id']}",  # invoice_payload
                provider_token=config.provider_tokens['balance'].get(text),  # provider_token
                currency=last_balance['currency']['name'],  # currency
                prices=prices,  # prices
                photo_url=company_data['logo'].replace('http:', 'https:'),
                photo_height=512,  # !=0/None or picture won't be shown
                photo_width=512,
                photo_size=512,
                is_flexible=False,  # True If you need to set up Shipping Fee
                start_parameter='time-machine-example',
                need_name=False
            )
        else:
            msg = messages.balance_payment_type_msg.get(lang)
            keyb = payment_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_payment_type)
    except Exception as e:
        print(e)


#* Send
def get_send_currency_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [currency_type_texts.get('fiat', {}).get(lang), currency_type_texts.get('crypto', {}).get(lang)]:
            currency_type = 'fiat'
            if currency_type_texts.get('crypto', {}).get(lang) == text:
                currency_type = 'crypto'
            update_send(user_id=chat_id, currency_type=currency_type, get_data='yes')
            msg = messages.send_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type=currency_type, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency)
        elif text == back_text.get(lang):
            msg = messages.get_section_msg.get(lang)
            keyb = balance_section_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_balance_section)
        else:
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency_type)
    except Exception as e:
        print(e)


#* Send
def get_send_currency(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency_type)
        elif text.endswith(prev_text.get(lang)):
            send = update_send(user_id=chat_id, get_data='yes')
            page = text.split(' ')[0]
            msg = messages.send_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=send['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency)
        elif text.startswith(next_text.get(lang)):
            send = update_send(user_id=chat_id, get_data='yes')
            page = text.split(' ')[-1]
            msg = messages.send_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=send['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_send_currency)
            else:
                currency_id = currency['results'][0]['id']
                update_send(user_id=chat_id, update_type='plus', currency_id=currency_id)
                msg = messages.send_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'send', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_send_input)
    except Exception as e:
        print(e)


#* Send
def get_send_input(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.send_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type='fiat', status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_currency)
        else:
            amount_input = text.replace(' ', '')
            if amount_input.isdigit():
                balance = check_balance_for_send(user_id=chat_id)
                if balance > float(amount_input):
                    update_send(user_id=chat_id, amount=amount_input, get_data='yes')
                    msg = messages.send_hash_msg.get(lang)
                    keyb = back_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_send_hash)
                else:
                    msg = messages.no_balance_msg.get(lang)
                    keyb = balance_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, balance_menu)
            else:
                msg = messages.send_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'send', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_send_input)
    except Exception as e:
        print(e)


#* Send
def get_send_hash(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.send_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'send', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_input)
        else:
            if check_hash(text.strip()):
                send = update_send(user_id=chat_id, hash_code=text.strip(), get_data='yes')
                send_id = send['id']
                msg = messages.send_bill_msg.get(lang)
                msg = f'<a href="{config.site_url}/bill/send/{send_id}/">{msg}</a>'
                keyb = confirmation_btns(lang)
                send_msg = bot.reply_to(message, msg, reply_markup=keyb, parse_mode='html')
                bot.register_next_step_handler(message, confirm_send)
                message_id = send_msg.message_id
                update_send(user_id=chat_id, message_id=message_id)
            else:
                msg = messages.hash_not_found_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_send_hash)
    except Exception as e:
        print(e)


#* Send
def confirm_send(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.send_hash_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_send_hash)
        elif text == confirmation_texts.get('confirm', {}).get(lang):
            send = update_send(user_id=chat_id, confirmed='yes', get_data='yes')
            send_id = send['id']
            msg = messages.send_bill_msg.get(lang)
            msg = f'<a href="{config.site_url}/bill/send/{send_id}/?viewer=receiver">{msg}</a>'
            keyb = accept_send_btns(lang, chat_id, send['id'])
            bot.send_message(send['id_to'], msg, reply_markup=keyb, parse_mode='html')

            msg = messages.send_confirmed_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == confirmation_texts.get('deny', {}).get(lang):
            msg = messages.send_canceled_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
        else:
            send = update_send(user_id=chat_id, get_data='yes')
            amount = send['amount']
            if amount > 1:
                if are_decimal_digits_zero(amount):
                    amount = '{:7,.0f}'.format(amount)
                else:
                    amount = '{:7,.3f}'.format(amount)
            msg = f"Валюта отправки: *{send['currency']['name']}*\n"
            msg += f"Сумма отправки: *{send['amount']} {send['currency']['name']}*\n"
            msg += f"Хеш пользователья: `{send['hash_to']}`\n"
            keyb = confirmation_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb, parse_mode='Markdown')
            bot.register_next_step_handler(message)
    except Exception as e:
        print(e)


#! History
def get_history_currency_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [currency_type_texts.get('fiat', {}).get(lang), currency_type_texts.get('crypto', {}).get(lang)]:
            currency_type = 'fiat'
            if currency_type_texts.get('crypto', {}).get(lang) == text:
                currency_type = 'crypto'
            msg = messages.history_msg.get(lang) + "\n"
            history = user_exchanges(chat_id, currency_type)
            for item in history:
                currency_from = item['currency_from']['name']
                currency_to = item['currency_to']['name']
                
                amount_input = item['amount_input']
                if amount_input > 1:
                    if are_decimal_digits_zero(amount_input):
                        amount_input = '{:7,.0f}'.format(amount_input).strip()
                    else:
                        amount_input = '{:7,.3f}'.format(amount_input).strip()
                
                amount_output = item['amount_output']
                if amount_output > 1:
                    if are_decimal_digits_zero(amount_output):
                        amount_output = '{:7,.0f}'.format(amount_output).strip()
                    else:
                        amount_output = '{:7,.3f}'.format(amount_output).strip()
                
                msg += f"<b>{amount_input}</b> {currency_from} - <b>{amount_output}</b> {currency_to}\n"

            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb, parse_mode='html')
            bot.register_next_step_handler(message, get_history_currency_type)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.history_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_history_currency_type)
    except Exception as e:
        print(e)


#? Withdraw
def get_withdraw_currency_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text in [currency_type_texts.get('fiat', {}).get(lang), currency_type_texts.get('crypto', {}).get(lang)]:
            currency_type = 'fiat'
            if currency_type_texts.get('crypto', {}).get(lang) == text:
                currency_type = 'crypto'
            update_withdraw(user_id=chat_id, currency_type=currency_type)
            msg = messages.withdraw_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type=currency_type, status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency_type)
    except Exception as e:
        print(e)


#? Withdraw
def get_withdraw_currency(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.currency_type_msg.get(lang)
            keyb = currency_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency_type)
        elif text.endswith(prev_text.get(lang)):
            withdraw = update_withdraw(user_id=chat_id, get_data='yes')
            page = text.split(' ')[0]
            msg = messages.withdraw_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=withdraw['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency)
        elif text.startswith(next_text.get(lang)):
            withdraw = update_withdraw(user_id=chat_id, get_data='yes')
            page = text.split(' ')[-1]
            msg = messages.withdraw_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type=withdraw['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_balance_currency)
            else:
                currency_id = currency['results'][0]['id']
                update_withdraw(user_id=chat_id, currency_id=currency_id)
                msg = messages.withdraw_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'withdraw', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_input)
    except Exception as e:
        print(e)


#? Withdraw
def get_withdraw_input(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            withdraw = update_withdraw(user_id=chat_id, get_data='yes')
            msg = messages.withdraw_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type=withdraw['currency_type'], status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_currency)
        else:
            amount_input = text.replace(' ', '')
            if amount_input.isdigit():
                permissions = get_subscription_permissions(user_id=chat_id)
                amount_input = float(amount_input) * permissions['withdraw_fee']
                balance = check_balance_for_withdraw(user_id=chat_id)
                if balance > amount_input:
                    withdraw = update_withdraw(user_id=chat_id, amount=amount_input, fees=permissions['withdraw_fee'], get_data='yes')
                    if withdraw['currency_type'] == 'fiat':
                        msg = messages.withdraw_card_msg.get(lang)
                        keyb = back_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, get_withdraw_card)
                    else:
                        msg = messages.withdraw_wallet_msg.get(lang)
                        keyb = back_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, get_withdraw_wallet)
                else:
                    msg = messages.no_balance_msg.get(lang)
                    keyb = balance_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, balance_menu)
            else:
                msg = messages.withdraw_input_msg.get(lang)
                keyb = stock_btns(chat_id, 'withdraw', lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_input)
    except Exception as e:
        print(e)


#? Withdraw
def get_withdraw_card(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.withdraw_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'withdraw', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_input)
        else:
            text_array = text.split(' ')
            if len(text_array) > 2:
                card_name = f"{text_array[-2]} {text_array[-1]}"
                card_number = ' '.join(text_array[:-2]).replace(' ', '')
                if card_name.replace(' ', '').isalpha() and card_number.isdigit():
                    withdraw = update_withdraw(user_id=chat_id, credit_card=text, get_data='yes')
                    withdraw_id = withdraw['id']
                    msg = messages.withdraw_bill_msg.get(lang)
                    msg = f'<a href="{config.site_url}/bill/withdraw/{withdraw_id}/">{msg}</a>'
                    keyb = confirmation_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb, parse_mode='html')
                    bot.register_next_step_handler(message, confirm_withdraw)
                else:
                    msg = messages.withdraw_card_msg.get(lang)
                    keyb = back_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_withdraw_card)
            else:
                msg = messages.withdraw_card_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_card)
    except Exception as e:
        print(e)


#? Withdraw
def get_withdraw_wallet(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.withdraw_input_msg.get(lang)
            keyb = stock_btns(chat_id, 'withdraw', lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_withdraw_input)
        else:
            withdraw = update_withdraw(user_id=chat_id, wallet=text, get_data='yes')
            withdraw_id = withdraw['id']
            msg = messages.withdraw_bill_msg.get(lang)
            msg = f'<a href="{config.site_url}/bill/withdraw/{withdraw_id}/">{msg}</a>'
            keyb = confirmation_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb, parse_mode='html')
            bot.register_next_step_handler(message, confirm_withdraw)
    except Exception as e:
        print(e)


#? Withdraw
def confirm_withdraw(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text.strip()
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            withdraw = update_withdraw(user_id=chat_id, get_data='yes')
            if withdraw['currency_type'] == 'fiat':
                msg = messages.withdraw_card_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_card)
            else:
                msg = messages.withdraw_wallet_msg.get(lang)
                keyb = back_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_withdraw_wallet)
        elif text == confirmation_texts.get('confirm', {}).get(lang):
            withdraw = update_withdraw(user_id=chat_id, confirmed='yes', get_data='yes')
            # To Group
            msg = f"#️⃣ Номер заявки: {withdraw['id']}\n"
            msg += f"📎 ID пользователья: {chat_id}\n"
            msg += f"💵 Валюта обмена: {withdraw['currency']['name']}\n"
            msg += f"🔢 Сумма обмена: {withdraw['amount']}\n"
            if withdraw['credit_card']:
                msg += f"💳 Карта пополнения: {withdraw['credit_card']}\n"
            elif withdraw['wallet']:
                msg += f"💳 Кошелёк пополнения: {withdraw['wallet']}\n"
            keyb = accept_withdraw_btns(lang, user_id=chat_id, withdraw_id=withdraw['id'])
            bot.send_message(config.withdraw_group_id[withdraw['currency_type']], msg, reply_markup=keyb)

            # To User
            msg = messages.withdraw_send_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        elif text == confirmation_texts.get('deny', {}).get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
    except Exception as e:
        print(e)


#* Settings
def get_settings_menu(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == settings_texts.get('cabinet', {}).get(lang):
            user_data = get_trader_data(user_id=chat_id)
            msg = f"ID: *{user_data['id']}*\n"
            msg += f"Имя пользователья: *{user_data['username']}*\n"
            msg += f"Имя: *{user_data['first_name']}*\n"
            msg += f"Фамилия: *{user_data['last_name']}*\n"
            msg += f"Почта: *{user_data['email']}*\n"
            msg += f"День рождения: *{user_data['date_of_birth']}*\n"
            msg += f"Дата регистрации: *{user_data['date_joined']}*\n"
            msg += f"Ваш хеш: `{user_data['hash']}`\n"
            msg += f"Статус: *{user_data['subscription']['status'].capitalize()} user*\n"
            msg += f"\n"
            msg += f"Чтобы изменить данные посетите свой профиль на нашем сайте"
            keyb = profile_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb, parse_mode='Markdown')

            msg = messages.cabinet_msg.get(lang)
            keyb = cabinet_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_cabinet_menu)
        elif text == settings_texts.get('change_language', {}).get(lang):
            msg = messages.language_msg
            keyb = language_btns()
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_language)
        elif text == settings_texts.get('change_country', {}).get(lang):
            msg = messages.get_city_msg.get(lang)
            keyb = city_btns(lang, page=1)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_city)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.settings_msg.get(lang)
            keyb = settings_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_settings_menu)
    except Exception as e:
        print(e)


#* Settings
def get_cabinet_menu(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == cabinet_texts.get('username', {}).get(lang):
            msg = messages.get_username_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_username)
        elif text == cabinet_texts.get('password', {}).get(lang):
            msg = messages.get_password_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_password)
        elif text == cabinet_texts.get('logout', {}).get(lang):
            msg = messages.confirm_logout_msg.get(lang)
            keyb = confirmation_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, confirm_logout)
        elif text == back_text.get(lang):
            msg = messages.settings_msg.get(lang)
            keyb = settings_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_settings_menu)
        else:
            user_data = get_trader_data(user_id=chat_id)
            msg = f"ID: *{user_data['id']}*\n"
            msg += f"Имя пользователья: *{user_data['username']}*\n"
            msg += f"Имя: *{user_data['first_name']}*\n"
            msg += f"Фамилия: *{user_data['last_name']}*\n"
            msg += f"Почта: *{user_data['email']}*\n"
            msg += f"День рождения: *{user_data['date_of_birth']}*\n"
            msg += f"Дата регистрации: *{user_data['date_joined']}*\n"
            msg += f"Ваш хеш: `{user_data['hash']}`\n"
            msg += f"Статус: *{user_data['subscription']['status'].capitalize()} user*\n"
            msg += f"\n"
            msg += f"Чтобы изменить данные посетите свой профиль на нашем сайте"
            keyb = profile_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb, parse_mode='Markdown')

            msg = messages.cabinet_msg.get(lang)
            keyb = cabinet_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_cabinet_menu)
    except Exception as e:
        print(e)


#* Settings
def confirm_logout(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            user_data = get_trader_data(user_id=chat_id)
            msg = f"ID: *{user_data['id']}*\n"
            msg += f"Имя пользователья: *{user_data['username']}*\n"
            msg += f"Имя: *{user_data['first_name']}*\n"
            msg += f"Фамилия: *{user_data['last_name']}*\n"
            msg += f"Почта: *{user_data['email']}*\n"
            msg += f"День рождения: *{user_data['date_of_birth']}*\n"
            msg += f"Дата регистрации: *{user_data['date_joined']}*\n"
            msg += f"Ваш хеш: `{user_data['hash']}`\n"
            msg += f"Статус: *{user_data['subscription']['status'].capitalize()} user*\n"
            msg += f"\n"
            msg += f"Чтобы изменить данные посетите свой профиль на нашем сайте"
            keyb = profile_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb, parse_mode='Markdown')

            msg = messages.cabinet_msg.get(lang)
            keyb = cabinet_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_cabinet_menu)
        elif text == confirmation_texts.get('confirm', {}).get(lang):
            msg = messages.auth_msg.get(lang)
            keyb = auth_btns()
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_auth_options)
        elif text == confirmation_texts.get('deny', {}).get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.confirm_logout_msg.get(lang)
            keyb = confirmation_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message)
    except Exception as e:
        print(e)


#* Settings
def get_auth_options(message: Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == auth_texts.get('sign_in', {}).get(lang):
            msg = messages.login_username_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb, parse_mode='html')
            bot.register_next_step_handler(message, get_login_data)
        elif text == auth_texts.get('sign_up', {}).get(lang):
            logout_user(chat_id)
            msg = messages.logout_done_msg.get(lang)
            bot.send_message(chat_id, msg)

            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            lang_code = message.from_user.language_code
            update_user(user_id=chat_id, username=username, first_name=first_name, last_name=last_name, chat_id=chat_id, lang_code=lang_code)
            msg = messages.language_msg
            keyb = language_btns()
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_language)
        else:
            msg = messages.auth_msg.get(lang)
            keyb = auth_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_auth_options)
    except Exception as e:
        print(e)


#* Settings
def get_login_data(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if message.content_type == 'text':
            if text == back_text.get(lang):
                msg = messages.auth_msg.get(lang)
                keyb = auth_btns()
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_auth_options)
            else:
                if len(text.split('-')) == 2:
                    username = text.split('-')[0].strip()
                    password = text.split('-')[1].strip()
                    username_valid = check_username(username, chat_id)
                    if username_valid == 'no':
                        password_valid = check_password(username, password)
                        if password_valid['password_valid'] == 'yes':
                            logout_user(chat_id)
                            msg = messages.logout_done_msg.get(lang)
                            bot.send_message(chat_id, msg)

                            username = message.from_user.username
                            first_name = message.from_user.first_name
                            last_name = message.from_user.last_name
                            lang_code = message.from_user.language_code
                            update_user(user_id=chat_id, username=username, first_name=first_name, last_name=last_name, chat_id=chat_id, lang_code=lang_code, trader_id=password_valid['trader_id'])

                            msg = messages.language_msg
                            keyb = language_btns()
                            bot.reply_to(message, msg, reply_markup=keyb)
                            bot.register_next_step_handler(message, get_language)
                        else:
                            msg = messages.login_data_invalid.get(lang)
                            keyb = back_btns(lang)
                            bot.reply_to(message, msg, reply_markup=keyb)
                            bot.register_next_step_handler(message, get_login_data)
                    else:
                        msg = messages.username_not_found_msg.get(lang)
                        keyb = back_btns(lang)
                        bot.reply_to(message, msg, reply_markup=keyb)
                        bot.register_next_step_handler(message, get_login_data)
                else:
                    msg = messages.login_data_invalid.get(lang)
                    keyb = back_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_login_data)
        else:
            msg = messages.get_username_msg.get(lang)
            keyb = back_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_login_data)
    except Exception as e:
        print(e)


#! Subscription
def subscription_menu(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == subscription_menu_texts.get('advantages').get(lang):
            subscription_types = get_subscription_types(status='all')
            for item in subscription_types:
                msg = item[f'description_{lang}']
                msg = "\n".join(msg.split('<br>'))
                bot.send_message(chat_id, msg, parse_mode='html')
            msg = messages.subscription_menu_msg.get(lang)
            keyb = subscription_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, subscription_menu)
        elif text in [subscription_menu_texts.get('check_subscription').get(lang), subscription_menu_texts.get('new_subscription').get(lang)]:
            subscription = get_trader_data(chat_id)['subscription']
            if subscription['status'] in ['pro', 'medium']:
                msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                msg += f"{messages.subscription_next_payment_msg.get(lang)}: {subscription['next_payment']}"
                keyb = subscription_update_btns(lang)
            else:
                if text == subscription_menu_texts.get('new_subscription').get(lang):
                    msg = messages.subscription_period_msg.get(lang)
                    keyb = subscription_period_btns(lang)
                    bot.reply_to(message, msg, reply_markup=keyb)
                    bot.register_next_step_handler(message, get_subscription_period)
                else:
                    msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                    msg += messages.subscription_apply_msg.get(lang)
                    keyb = subscription_new_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_action)
        elif text == subscription_menu_texts.get('reff_link').get(lang):
            explanation = get_explanations('reff_link')
            msg = explanation[0][f'description_{lang}']
            msg = "\n".join(msg.split('<br>'))
            bot.send_message(chat_id, msg, parse_mode='html')

            user_data = get_trader_data(user_id=chat_id)
            msg = messages.reff_link_msg.get(lang)
            msg += "\n\n"
            msg += f"{config.site_url}/reff_link/{user_data['hash']}/"
            bot.send_message(chat_id, msg)
        elif text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.send_message(chat_id, msg, reply_markup=keyb)
        else:
            msg = messages.subscription_menu_msg.get(lang)
            keyb = subscription_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, subscription_menu)
    except Exception as e:
        print(e)


#! Subscription
def get_subscription_action(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.subscription_menu_msg.get(lang)
            keyb = subscription_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, subscription_menu)
        elif text in [subscription_update_texts.get(lang), subscription_menu_texts.get('new_subscription').get(lang)]:
            msg = messages.subscription_period_msg.get(lang)
            keyb = subscription_period_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_period)
        else:
            subscription = get_trader_data(chat_id)['subscription']
            if subscription['status'] in ['pro', 'medium']:
                msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                msg += f"{messages.subscription_next_payment_msg.get(lang)}: {subscription['next_payment']}"
                keyb = subscription_update_btns(lang)
            else:
                msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                msg += messages.subscription_apply_msg.get(lang)
                keyb = subscription_new_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_action)
    except Exception as e:
        print(e)


#! Subscription
def get_subscription_period(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            subscription = get_trader_data(chat_id)['subscription']
            if subscription['status'] in ['pro', 'medium']:
                msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                msg += f"{messages.subscription_next_payment_msg.get(lang)}: {subscription['next_payment']}"
                keyb = subscription_update_btns(lang)
            else:
                msg = f"{messages.subscription_status_msg.get(lang)}: {subscription['status'].capitalize()} user\n"
                msg += messages.subscription_apply_msg.get(lang)
                keyb = subscription_new_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_action)
        else:
            text = text.split('(')[0].strip()
            subscription_period = get_subscription_periods(text)
            if len(subscription_period) == 0:
                msg = messages.subscription_period_msg.get(lang)
                keyb = subscription_period_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_subscription_period)
            else:
                subscription_period_id = subscription_period[0]['id']
                update_subscription(user_id=chat_id, subscription_period_id=subscription_period_id)
                msg = messages.subscription_type_msg.get(lang)
                keyb = subscription_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_subscription_type)
    except Exception as e:
        print(e)


#! Subscription
def get_subscription_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.subscription_period_msg.get(lang)
            keyb = subscription_period_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_period)
        else:
            text = text.replace('Oval ', '').replace(' 💎', '').lower()
            subscription_type = get_subscription_types(text)
            if len(subscription_type) == 0:
                msg = messages.subscription_type_msg.get(lang)
                keyb = subscription_type_btns(lang)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_subscription_type)
            else:
                subscription_type_id = subscription_type[0]['id']
                update_subscription(user_id=chat_id, subscription_type_id=subscription_type_id)
                msg = messages.subscription_currency_msg.get(lang)
                subscription = get_trader_data(user_id=chat_id)['subscription']['status']
                keyb = currency_btns(lang, currency_type='fiat', status=subscription)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_subscription_currency)
    except Exception as e:
        print(e)


#! Subscription
def get_subscription_currency(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.subscription_type_msg.get(lang)
            keyb = subscription_type_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_type)
        elif text.endswith(prev_text.get(lang)):
            page = text.split(' ')[0]
            msg = messages.subscription_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type='fiat', status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_currency)
        elif text.startswith(next_text.get(lang)):
            page = text.split(' ')[-1]
            msg = messages.subscription_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, page=int(page), currency_type='fiat', status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_currency)
        else:
            currency = get_currency_by_name(text)
            if currency['count'] == 0:
                msg = messages.no_currency_msg.get(lang)
                bot.reply_to(message, msg)
                bot.register_next_step_handler(message, get_subscription_currency)
            else:
                currency_id = currency['results'][0]['id']
                update_subscription(user_id=chat_id, currency_id=currency_id)
                msg = messages.subscription_payment_type_msg.get(lang)
                keyb = payment_type_btns(lang, text)
                bot.reply_to(message, msg, reply_markup=keyb)
                bot.register_next_step_handler(message, get_subscription_payment_type)
    except Exception as e:
        print(e)


#! Subscription
def get_subscription_payment_type(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.subscription_currency_msg.get(lang)
            subscription = get_trader_data(user_id=chat_id)['subscription']['status']
            keyb = currency_btns(lang, currency_type='fiat', status=subscription)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_currency)
        elif text in payment_type_texts:
            last_subscription = update_subscription(user_id=chat_id, payment_type=text, get_data='yes')
            company_data = load_company_data()

            prices = [
                LabeledPrice(label=messages.subscription_invoice_msg.get(lang), amount=int(last_subscription['price'])*100),
            ]

            bot.send_invoice(
                chat_id=message.chat.id,  # chat_id
                title=f"{company_data['name']}",  # title
                description=messages.balance_invoice_description_msg.get(lang),  # description
                invoice_payload=f"subscription_{last_subscription['id']}",  # invoice_payload
                provider_token=config.provider_tokens['subscription'].get(text),  # provider_token
                currency=last_subscription['currency']['name'],  # currency
                prices=prices,  # prices
                photo_url=company_data['logo'].replace('http:', 'https:'),
                photo_height=512,  # !=0/None or picture won't be shown
                photo_width=512,
                photo_size=512,
                is_flexible=False,  # True If you need to set up Shipping Fee
                start_parameter='time-machine-example',
                need_name=False
            )
        else:
            msg = messages.subscription_payment_type_msg.get(lang)
            keyb = payment_type_btns(lang, text)
            bot.reply_to(message, msg, reply_markup=keyb)
            bot.register_next_step_handler(message, get_subscription_payment_type)
    except Exception as e:
        print(e)


#? Reff link


#* Tex work
def get_tex_work(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        lang = get_user_lang(chat_id)
        if text == back_text.get(lang):
            msg = messages.main_menu_msg.get(lang)
            keyb = main_menu_btns(lang)
            bot.reply_to(message, msg, reply_markup=keyb)
        else:
            tex_work = get_tex_works(name=text)
            if tex_work:
                msg = tex_work[0][f'description_{lang}']
                msg = "\n".join(msg.split('<br>'))
            else:
                msg = messages.tex_work_msg.get(lang)
            keyb = tex_work_btns(lang)
            if tex_work[0]['poster']:
                tex_message = bot.send_photo(chat_id, tex_work[0]['poster'], caption=msg, reply_markup=keyb, parse_mode='html')
            else:
                tex_message = bot.send_message(chat_id, msg, reply_markup=keyb, parse_mode='html')
            bot.register_next_step_handler(tex_message, get_tex_work)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def answer(call: types.CallbackQuery):
    try:
        print(call.data)
        chat_id = call.json['message']['chat']['id']
        message_id = call.message.message_id
        
        if call.data.startswith('confirm_withdraw_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            withdraw_id = call.data.split('_')[3]
            update_withdraw(user_id=user_id, withdraw_id=withdraw_id, accepted='yes')
            msg = messages.withdraw_accepted_msg.get(lang)
            bot.send_message(user_id, msg)

            # Change btns
            keyb = accepted_btns(lang)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data.startswith('deny_withdraw_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            msg = messages.withdraw_denied_msg.get(lang)
            bot.send_message(user_id, msg)

            # Change btns
            keyb = denied_btns(lang)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data.startswith('confirm_balance_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            balance_id = call.data.split('_')[3]
            update_balance(user_id=user_id, balance_id=balance_id, payed='yes')
            msg = messages.balance_accepted_msg.get(lang)
            bot.send_message(user_id, msg)

            # Change btns
            keyb = accepted_btns(lang)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data.startswith('deny_balance_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            msg = messages.balance_denied_msg.get(lang)
            bot.send_message(user_id, msg)

            # Change btns
            keyb = denied_btns(lang)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data.startswith('confirm_send_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            send_id = call.data.split('_')[3]
            send = update_send(user_id=user_id, send_id=send_id, accepted='yes', get_all='yes')
            if send.get('error') == 'balance':
                msg = messages.sender_no_balance_msg.get(lang)
                bot.send_message(chat_id, msg)
            else:
                msg = messages.send_accepted_msg.get(lang)
                bot.send_message(user_id, msg)

                # Change btns
                keyb = accepted_btns(lang)
                bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data.startswith('deny_send_'):
            # Send message to user
            user_id = call.data.split('_')[2]
            lang = get_user_lang(user_id)
            send_id = call.data.split('_')[3]
            update_send(user_id=user_id, send_id=send_id, accepted='no')
            msg = messages.send_denied_msg.get(lang)
            bot.send_message(user_id, msg)

            # Change btns
            keyb = denied_btns(lang)
            bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyb)

        elif call.data == 'already_accepted':
            bot.answer_callback_query(call.id, accepted_text.get('ru'))

        elif call.data == 'already_denied':
            bot.answer_callback_query(call.id, denied_text.get('ru'))

        elif call.data.startswith('exchange_rate_'):
            bot.delete_message(chat_id, message_id)

            lang = get_user_lang(chat_id)
            exchange_id = call.data.split('_')[2]
            rate = call.data.split('_')[3]
            update_exchange(user_id=chat_id, exchange_id=exchange_id, rate=rate, get_data='yes')
            msg = messages.exchange_bill_msg.get(lang)
            msg = f'<a href="{config.site_url}/bill/exchange/{exchange_id}/">{msg}</a>'
            keyb = confirmation_btns(lang)
            message = bot.send_message(chat_id, msg, reply_markup=keyb, parse_mode='html')
            bot.register_next_step_handler(message, confirm_exchange)
    
    except Exception as e:
        print(e)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=config.shipping_options,
                              error_message='Oh, seems like our Dog couriers are having a lunch right now. Try again later!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message: Message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if 'balance_' in message.successful_payment.invoice_payload:
        balance_id = message.successful_payment.invoice_payload.replace('balance_', '')
        balance = update_balance(user_id=chat_id, balance_id=balance_id, confirmed='yes', payed='yes', get_data='yes')
        keyb = main_menu_btns(lang)
        bot.send_message(message.chat.id, messages.balance_payed_msg.get(lang), reply_markup=keyb)

        msg = f"{messages.balance_payed_msg.get(lang)} ({messages.balance_bill_msg})"
        bot.send_message(config.balance_group_id.get(balance['currency_type']), msg)
    
    elif 'subscription_' in message.successful_payment.invoice_payload:
        subscription_id = message.successful_payment.invoice_payload.replace('subscription_', '')
        subscription = update_subscription(user_id=chat_id, subscription_id=subscription_id, payed='yes', get_data='yes')
        keyb = main_menu_btns(lang)
        bot.send_message(message.chat.id, messages.subscription_payed_msg.get(lang), reply_markup=keyb)

        msg = f"{messages.subscription_payed_msg.get(lang)} ({messages.subscription_bill_msg})"
        bot.send_message(config.balance_group_id.get(subscription['currency']['currency_type']), msg)


bot.polling(none_stop=True)
