# -*- coding: utf-8 -*-
"""
Модуль для взаимодествия с компаниями БД.
"""
import sqlite3
import config


def get_companies_list(short_name:str, offset:int):
    """
    Аргументы: Начало имени компании, сдвиг относительно начала.
    Возвращает: 5 компаний, которые начинаются также.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute(fr'''SELECT Company.name, Company.symbol, Exchange.name
                        FROM Company JOIN Exchange ON Company.exchange_id = Exchange.id
                        WHERE Company.name LIKE '%{short_name}%' ORDER BY Company.id ASC LIMIT 5 OFFSET ?''',
                    (offset,))
        companies = cur.fetchall()
        return companies

def get_company_ticker(name:str)->str:
    """
    Аргументы: Начало имени компании, сдвиг относительно начала.
    Возвращает: 5 компаний, которые начинаются также.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT symbol FROM Company WHERE name = ?",(name,))
        ticker = cur.fetchone()[0]
    return ticker
