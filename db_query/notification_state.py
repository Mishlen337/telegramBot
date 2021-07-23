# -*- coding: utf-8 -*-
"""
Модуль для изменения и установки состояния уведомления
"""
import sqlite3
import config

def get_notification_state(user_chat_id:int):
    """
    Аргументы: чат Id пользователя.
    Возвращает: текущее состояние уведомления.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT notification_state FROM User WHERE user_chat_id = ?", (user_chat_id,))
        return cur.fetchone()[0]

def get_notification_time(user_chat_id:int):
    """
    Аргументы: чат Id пользователя.
    Возвращает: текущее время уведомления.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT notification_time FROM User WHERE user_chat_id = ?", (user_chat_id,))
        return cur.fetchone()[0]

def set_notification_state(user_chat_id:int, state:int):
    """
    Аргументы: чат Id пользователя.
    Цель: изменение текущего состояния уведомления.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_state = ? WHERE user_chat_id = ?", (state,user_chat_id))
        conn.commit()

def set_notification_time(user_chat_id:int, time: str):
    """
    Аргументы: чат Id пользователя.
    Цель: изменение текущего времени уведомления.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE User SET notification_time = ? WHERE user_chat_id = ?", (time,user_chat_id))
        conn.commit()
