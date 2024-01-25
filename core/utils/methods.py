import json
import requests


async def get_payment_methods():
    url = "https://api2.bybit.com/fiat/otc/configuration/queryAllPaymentList"
    response = requests.post(url).json()
    tickets = response['result']['paymentConfigVo']
    data = dict()

    for ticket in tickets:
        data[ticket['paymentType']] = ticket['paymentName']

    with open('tmp/bybit_payments.json', 'w') as file:
        json.dump(data, file, indent=4)


def pay_method_bybit(method: str) -> str:
    with open('tmp/bybit_payments.json', 'r') as file:
        data = json.load(file)
        return data[method]


def trade_type_converter(method: str) -> bool:
    if method.upper() == 'SELL':
        return False
    else:
        return True


def type_trade_bybit(method):
    methods_str = {'SELL': '0',
                   'BUY': '1'}
    methods_int = {'0': 'SELL',
                   '1': 'BUY'}
    if len(method) > 1:
        return methods_str[method.upper()]
    else:
        return methods_int[method]


def coin_paxful(coin: str) -> int:
    coins = {'USDT': 4,
             'BTC': 1,
             'USDC': 7}
    return coins[coin]
