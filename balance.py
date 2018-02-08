import argparse
import yaml

from time import sleep
from sys import platform
from os import system
from datetime import datetime
from bittrex_balance import MyBittrex

HEADER = '''\
_________                        __        ___.          .__
\_   ___ \_______ ___.__._______/  |_  ____\_ |__ _____  |  | _____    ____   ____  ____
/    \  \/\_  __ <   |  |\____ \   __\/  _ \| __ \\__  \ |  | \__  \  /    \_/ ___\/ __ \
\     \____|  | \/\___  ||  |_> >  | (  <_> ) \_\ \/ __ \|  |__/ __ \|   |  \  \__\  ___/
 \______  /|__|   / ____||   __/|__|  \____/|___  (____  /____(____  /___|  /\___  >___  >
        \/        \/     |__|                   \/     \/          \/     \/     \/    \/

         Created by: Ijesh Giri
'''

def print_header():
    print(HEADER)

def process_args():
    parser = argparse.ArgumentParser(description='Watch balance across multiple exchanges!')
    parser.add_argument('--config', default= 'config.yaml',help ='locaion of the config yaml file')

    args = parser.parse_args()
    return args

def clear():
    """
    Output: Clears the terminal
    """
    if platform in ("linux", "linux2", "darwin"):
        system("clear")
    elif platform == "win32":
        system("cls")
    else:
        print("Unsupported command for the system!")

from binance.client import Client
def main():
    args = process_args()
    with open(args.config) as keys:
        info_dict = yaml.load(keys)
        binance_key = info_dict['binance']['APIKey']
        binance_secret = info_dict['binance']['Secret']
        client = Client(binance_key, binance_secret)
        print("\nBinance")
        total = get_total(client)

        print("\nBittrex")
        bittrex_key = info_dict['bittrex']['APIKey']
        bittrex_secret = info_dict['bittrex']['Secret']
        myBittrex = MyBittrex(bittrex_key, bittrex_secret)
        total += myBittrex.get_balance()

        print("\n\nTotal: "+ str(round(total, 2)))

def watch_loop(client, sleep_time = 30):
    try:
        while True:
            total = get_total(client)
            print("Total balance: " + str(round(total, 2)) + " USD")
            sleep(sleep_time) #every 30 secs
            print("\n*****************************************************\n")
    except KeyboardInterrupt:
        clear()
        print_header()

def get_total(client):
    btc_price_usd = get_currency_price_in_usd(client, "BTC")
    eth_price_usd = get_currency_price_in_usd(client, "ETH")

    print("Fetched at: "+ str(datetime.now()))
    account_info = client.get_account()
    nonzero_balances = get_nonzero_balances(account_info['balances'])
    total = 0
    for key, value in nonzero_balances.iteritems():
        if(key == "BCX" or key == "SBTC"):
            continue
        currency_price_usd = 0.00
        try:
            currency_price_usd = get_currency_price_in_usd(client, key)
        except:
            try:
                currency_price_usd = get_currency_price_in_usd(client, key, "BTC") * btc_price_usd
            except:
                currency_price_usd = get_currency_price_in_usd(client, key, "ETH") * eth_price_usd
        symbolValue = value * currency_price_usd
        if(symbolValue > 1000):
            print(key + ": " + str(symbolValue) + " USD")
        total += symbolValue

    return total

def get_nonzero_balances(balances):
    nonzero_balances = {}
    for balance in balances:
        total = float(balance['free']) + float(balance['locked'])
        if(total > 0.0):
            nonzero_balances[balance['asset']] = total
        else:
            continue
    return nonzero_balances

def get_currency_price_in_usd(client, currency, base_currency="USDT"):
    currency_pair = "{}{}".format(currency, base_currency)
    api_response = client.get_symbol_ticker(symbol=currency_pair)
    return float(api_response['price'])

if __name__ == '__main__':
    print_header()
    main()
