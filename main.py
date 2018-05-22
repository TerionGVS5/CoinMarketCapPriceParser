import sqlite3
import requests
import datetime
from time import sleep


def fromUnixTimeToHumanString(seconds):
    return datetime.datetime.fromtimestamp(
        int(seconds)
    ).strftime('%Y-%m-%d %H:%M:%S')


def makeRequestGetData(start=1, count_in_db=0):
    #  The maximum number of results per call is 100.
    r = requests.get('https://api.coinmarketcap.com/v2/ticker/?start={}'.format(start))
    json_result = r.json()
    json_data = json_result['data']
    data_for_db = []
    for coin in json_data.values():
        symbol = coin['symbol']
        try:
            price = float(coin['quotes']['USD']['price'])
            time = fromUnixTimeToHumanString(coin['last_updated'])
            data_for_db.append((symbol, price, time))
        except TypeError:
            # for this situations Vcash (XVC) exp.
            # Please note that deposits and withdrawals are currently disabled on Poloniex due to maintenance.
            continue


    count_coins = json_result['metadata']['num_cryptocurrencies']
    count_in_db += len(data_for_db)
    return data_for_db, count_coins, count_in_db


def make_db():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS coins
                        (currency text, price real, time text)
                    """)
    conn.commit()
    cursor.execute("DELETE FROM coins")
    conn.commit()
    data, count_coins, count_in_db = makeRequestGetData()
    cursor.executemany("INSERT INTO coins VALUES (?,?,?)", data)
    conn.commit()
    while (count_in_db < count_coins):
        # Please limit requests to no more than 30 per minute.
        sleep(2)
        data, count_coins, count_in_db = makeRequestGetData(count_in_db+1, count_in_db)
        cursor.executemany("INSERT INTO coins VALUES (?,?,?)", data)
        conn.commit()

if __name__ == '__main__':
    make_db()
