# -*- coding: utf-8 -*-
"""
Модуль для изменения и извлечения текущего состояния.
"""
import sqlite3
import config
# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_chat_id):
    """
    Аргументы: чат Id пользователя.
    Возвращает: текущее состояние пользователя.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        cur.execute("SELECT state FROM User WHERE user_chat_id=?", (user_chat_id,))
        try:
            return cur.fetchone()[0]
        except TypeError:
            return config.States.S_START

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_chat_id, state):
    """
    Аргументы: чат Id пользователя.
    Цель изменение текущего состояние пользователя.
    """
    with sqlite3.connect(config.db_file) as conn:
        cur = conn.cursor()
        # Проверка на наличие user_chat_id в БД
        if cur.execute("SELECT user_chat_id FROM User WHERE user_chat_id=?", (user_chat_id,)).fetchone():
            # Обновляем значение state для полльзователя user_chat_id
            cur.execute("UPDATE User SET state = ? WHERE user_chat_id = ?", (state,user_chat_id))
        else:
            # Добавляем пользователя в БД
            cur.execute( "INSERT or IGNORE INTO User (user_chat_id, state) VALUES (?,?)", (user_chat_id, state) )
        conn.commit()
