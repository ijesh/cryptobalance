**************** Readme **************************
# Cryptobalance

Watch your balances across different cryptocurrency exchanges. Supported exchanges are: Bittrex, Binance and GDAX.

### Requirements
Pipenv must be installed to activate virtual env. Run *pipenv shell* before running the usage command.

Usage:
*python balance.py --config config.yaml*

Config.yaml file format:
`
binance:
  APIKey: [apikey-here]
  Secret: [secretkey-here]
bittrex:
  APIKey: [apikey-here]
  Secret: [secretkey-here]

`
