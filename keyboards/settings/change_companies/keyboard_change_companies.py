# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой изменения компаний.
"""
from telebot import types

def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры изменения компаний.
    Возвращает: Клавиатуру изменения компаний.
    """
    keyboard_change_companies = types.InlineKeyboardMarkup(row_width=1)
    button_add_companies = types.InlineKeyboardButton(text="Добавить компании",
                                                    callback_data="ДобавитьКомпании")
    button_delete_companies = types.InlineKeyboardButton(text="Удалить компании",
                                                    callback_data="УдалитьКомпании")
    keyboard_change_companies.add(button_add_companies, button_delete_companies)
    return keyboard_change_companies
