from pathlib import Path
from telebot.types import ShippingOption, LabeledPrice


site_url = "https://oval.lc"
# site_url = "http://127.0.0.1:8000"

token = "6589754747:AAE8qamcP3GJo-ppi5F5Ct4GcGruvmh8SeM" # Lc
# token = "6931094772:AAFb4FkDU0PGXALS-O9V0MKYUadQeKm52qg" # Uz

# provider_tokens = {
#     "balance": {
#         "Payme": "371317599:TEST:1705179496377",
#         "Click": "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065",
#     },
#     "subscription": {
#         "Payme": "387026696:LIVE:65b8b10aa7e94322f8b5ccbf",
#         "Click": "333605228:LIVE:22965_6793EAD7C975201173557FD96CF5A0F713CCB371",
#     }
# }

provider_tokens = {
    "balance": {
        "Payme": "387026696:LIVE:65a64e75afb6dba117258048",
        "Click": "333605228:LIVE:22965_6793EAD7C975201173557FD96CF5A0F713CCB371",
    },
    "subscription": {
        "Payme": "387026696:LIVE:65b8b10aa7e94322f8b5ccbf",
        "Click": "333605228:LIVE:22965_6793EAD7C975201173557FD96CF5A0F713CCB371",
    }
}

currency_providers = {
    "UZS": ["Payme", "Click"],
    "USD": ["Payme", "Click"],
}

send_group_id = {
    'fiat': '-4136911587',
    'crypto': '-4105790953',
}
withdraw_group_id = {
    'fiat': '-4147417798',
    'crypto': '-4167681023',
}
balance_group_id = {
    'fiat': '-4136512241',
    'crypto': '-4168654531',
}
exchange_group_id = {
    'fiat': '-1991572358',
    'crypto': '-1997971619',
}

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 100000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 100000))
]

dir_path = f"{Path(__file__).absolute()}"
dir_path = "/".join(dir_path.split('/')[:-1])
if dir_path == '':
    dir_path = f"{Path(__file__).absolute()}"
    dir_path = '\\'.join(dir_path.split('\\')[:-1])
