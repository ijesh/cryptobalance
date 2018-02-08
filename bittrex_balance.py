from bittrex.bittrex import Bittrex

class MyBittrex():
    def __init__(self, key, secret):
        self.mybittrex = Bittrex(key, secret)
        self.ethusd = float(self.get_usd("ETH")['result']['Last'])
        self.btcusd = float(self.get_usd("BTC")['result']['Last'])

    def get_balance(self):
        balances = self.mybittrex.get_balances()
        total = 0.0
        for balance in balances['result']:
            currency = balance['Currency']
            balance = float(balance['Balance'])
            if(balance > 0):
                try:
                    usd = 0.0
                    payload = self.get_usd(currency)
                    if(payload['success'] == False):
                        payload = self.get_usd(currency, "BTC")
                        if(payload['success'] == False):
                            payload = self.get_usd(currency, "ETH")
                            usd = balance * float(payload['result']['Last']) * self.ethusd
                        else:
                            usd = balance * float(payload['result']['Last']) * self.btcusd
                    else:
                        # print(payload)
                        usd = float(payload['result']['Last']) * balance
                    total += usd
                    print(currency + ": "+ str(usd) + " USD")
                except:
                    print("Error retrieving usd value for symbol: "+ currency)
        return total

    def get_usd(self, curr, base_currency = "USDT"):
        currency_pair = "{}-{}".format(base_currency, curr)
        return self.mybittrex.get_ticker(currency_pair)
