from keyboards.set import theory
from parse import stock_parse 
import config

def quote_answer_currency(company: str)->str:
    quote = stock_parse.parse_by_stockname(company)
    return f"Стоимость одной акции компании {company} - {quote[0]} {quote[1]}"

def quote_answer_ruble(company: str)->str:
    quote = stock_parse.parse_by_stockname(company)
    rubles = stock_parse.parse_currency(quote[1])
    quote_rubles = float(quote[0]) * rubles
    return f"Стоимость одной акции компании {company} - {quote_rubles:.2f} RUB"

def theory_answer_investment()->str:
    f = open(f"{config.theory_path}/lection2.txt")
    message = f.read()
    f.close()
    return message

def theory_answer_trading()->str:
    f = open(f"{config.theory_path}/lection1.txt")
    message = f.read()
    f.close()
    return message