from bs4 import BeautifulSoup
import config
import requests


def parse_by_stockname(stockname : str) -> tuple:
    """
    Функция принимает в качестве аргумента название котировки
    Функция возвращает кортеж из стоимости акции и валюты, в которой стоимость
    представлена
    """
    html = requests.get(f'{config.url_begining}{stockname}')
    soup = BeautifulSoup(html.text, 'html.parser')
    price = soup.find("span", {"class" : "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
    currency = soup.find("span", {"data-reactid" : "9"}).text.split()[-1]
    response = (price, currency)
    return response

print(parse_by_stockname("GAZP.ME"))