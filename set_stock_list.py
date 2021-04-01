import requests
from urllib.request import urlopen
import json
import config
import sqlite3
def list_companies():
    url = (f"https://financialmodelingprep.com/api/v3/stock/list?apikey={config.apikey}")
    response = urlopen(url)
    data = response.read().decode("utf-8")
    exchange_dict = {}
    data_list = json.loads(data)
    print(len(data_list))
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        for company in data_list:
            try:
                cur.execute("INSERT OR IGNORE INTO Exchange (name) VALUES (?)", (company['exchange'],) )
                cur.execute("SELECT id FROM Exchange WHERE name = ?", (company['exchange'],))
                exchange_id = cur.fetchone()[0]
                cur.execute( "INSERT OR IGNORE INTO Company2 (symbol, name, exchange_id) VALUES (?,?,?)", (company['symbol'], company['name'], exchange_id) )
                exchange_dict.setdefault(company['exchange'], 0)
                exchange_dict[company['exchange']] += 1
            except KeyError:
                pass
        conn.commit()
list_companies()
