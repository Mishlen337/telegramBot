from forex_python.converter import CurrencyRates

def parse_currency(currencyname : str) -> str:
    """
    Функция принимает на вход название валюты
    Функция возвращает ее стоимость (по отношению к USD)
    """
    converter = CurrencyRates()
    currency = converter.get_rates('USD')[currencyname]
    return currency
