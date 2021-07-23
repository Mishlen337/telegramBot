# -*- coding: utf-8 -*-
"""
Модуль для изменения и установки списка компаний для уведомления.
"""
import sqlite3
import config


def set_notification_member(user_chat_id:int, name:str):
    """
    Аргументы: чат Id пользователя.
    Цель: Устанавливает значения в таблицу Member для уведомления.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM Company WHERE name = ?", (name,))
        company_id = cur.fetchone()[0]
        cur.execute( "INSERT or IGNORE INTO Member (user_id, company_id) VALUES (?,?)", (user_id, company_id) )
        conn.commit()

def get_notification_list(user_chat_id:int):
    """
    Аргументы: чат Id пользователя.
    Возвращает: список компаний
    (Название - Тикер - Биржа) для уведомления,
    выбранный конкретным пользователем.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT Company.name, Company.symbol, Exchange.name 
                        FROM User JOIN Member JOIN Company JOIN Exchange 
                        ON Member.user_id = User.id AND Member.company_id = Company.id AND Company.exchange_id = Exchange.id 
                        WHERE User.user_chat_id = ?''', (user_chat_id,))
        rows = cur.fetchall()
        str_query = '\n'.join(map(' - '.join,rows))
        return str_query
    
def get_notification_companies(user_chat_id:int):
    """
    Аргументы: чат Id пользователя.
    Возвращает: список компаний
    (Название) для уведомления,
    выбранный конкретным пользователем.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute('''SELECT Company.name
                        FROM User JOIN Member JOIN Company JOIN Exchange 
                        ON Member.user_id = User.id AND Member.company_id = Company.id AND Company.exchange_id = Exchange.id 
                        WHERE User.user_chat_id = ?''', (user_chat_id,))
        rows = cur.fetchall()
        return rows

def delete_all_members(user_chat_id:int):
    """
    Аргументы: чат Id пользователя.
    Цель: Удаляет все компании пользователя для уведомления
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        cur.execute('''DELETE FROM Member WHERE user_id = ?''', (user_id,)) 
        conn.commit()

def delete_selectively_member(user_chat_id:int, name:str):
    """
    Аргументы: чат Id пользователя.
    Цель: Удаляет конкректную компанию пользователя для уведомления
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM Company WHERE name = ?", (name,))
        company_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM User WHERE user_chat_id = ?", (user_chat_id,))
        user_id = cur.fetchone()[0]
        #Проверка на существование пары (обрабатывается в bot.py через AttributeError)
        cur.execute("SELECT * FROM Member WHERE user_id = ? AND company_id = ?", (user_id,company_id))
        if not cur.fetchone():
            raise AttributeError
        cur.execute('''DELETE FROM Member WHERE user_id = ? AND company_id = ?''', (user_id,company_id)) 
        conn.commit()
