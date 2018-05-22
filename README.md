# CoinMarketCapPriceParser
Simple app that extract all prices of all coins from https://coinmarketcap.com/

This app use API from https://coinmarketcap.com/api/ 

App collect symbol coin (exp. BTC), price, and last update time in sqlite database.
The program takes into API limitations:
> Please limit requests to no more than 30 per minute.

## Installation
1. Install python3.6 and pip according official notes
2. Clone repository
3. Run this command in cloned folder 
> pip install -e .

**Better to use vitural env for your python**

Now you can run python command windows and call here and get your database:
> import CoinMarketCapPriceParser

> CoinMarketCapPriceParser.make_db()
