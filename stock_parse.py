from bs4 import BeautifulSoup
import config
import requests


def parse_by_stockname(stockname : str) -> str:
    html = requests.get(f'{config.url_begining}{stockname}')
    soup = BeautifulSoup(html.text, 'html.parser')
    response = soup.find("span", {"class" : "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
    return response

print(parse_by_stockname("TSLA"))