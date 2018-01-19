import argparse
import yaml

from time import sleep
from sys import platform
from os import system
from datetime import datetime

HEADER = '''\
_________                        __                         __         .__
\_   ___ \_______ ___.__._______/  |_  ______  _  _______ _/  |_  ____ |  |__
/    \  \/\_  __ <   |  |\____ \   __\/  _ \ \/ \/ /\__  \\\\   __\/ ___\|  |  \\
\     \____|  | \/\___  ||  |_> >  | (  <_> )     /  / __ \|  | \  \___|   Y  \\
\______  /|__|   / ____||   __/|__|   \____/ \/\_/  (____  /__|  \___  >___|  /
       \/        \/     |__|                             \/          \/     \/

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
        api_key = info_dict['binance']['APIKey']
        api_secret = info_dict['binance']['Secret']

        client = Client(api_key, api_secret)
        watch_loop(client, 5)

def watch_loop(client, sleep_time = 30):
    try:
        while True:
            print("Fetched at: "+ str(datetime.now()))
            account_info = client.get_account()
            nonzero_balances = get_nonzero_balances(account_info['balances'])
            btcusdt = btcusdt_price(client)
            sleep(sleep_time) #every 30 secs
            print("\n*****************************************************\n")

    except KeyboardInterrupt:
        clear()
        print_header()

def get_nonzero_balances(balances):
    nonzero_balances = {}
    for balance in balances:
        if(float(balance['free']) > 0.0):
            print(balance['free'] + " " + balance['asset'])
            nonzero_balances[balance['asset']] = float(balance['free'])

        if(float(balance['locked']) > 0.0):
            try:
                value = nonzero_balances[balance['asset']] + float(balance['locked'])
                print(str(value) + " " + balance['asset'])
                nonzero_balances[balance['asset']] = value
            except KeyError:
                print(balance['locked'] + " " + balance['asset'])
                nonzero_balances[balance['asset']] = float(balance['locked'])
        else:
            continue
    return nonzero_balances

def btcusdt_price(client):
    prices = client.get_symbol_ticker()
    for price in prices:
        if price['symbol'] == 'BTCUSDT':
            return float(price['price'])
    print('Price of BTCUSDT not found')
    return 0

if __name__ == '__main__':
    print_header()
    main()
