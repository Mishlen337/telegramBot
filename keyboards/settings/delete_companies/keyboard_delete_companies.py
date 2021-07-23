# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой удаления компаний.
"""
from telebot import types


def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры удаления компаний.
    Возвращает: Клавиатуру удаления компаний.
    """
    keyboard_delete_companies = types.InlineKeyboardMarkup(row_width=1)
    button_all = types.InlineKeyboardButton(text = "Удалить все", callback_data = "УдалитьВсе")
    button_selectively = types.InlineKeyboardButton(text = "Удалить выборочно", callback_data = "УдалитьВыборочно")
    keyboard_delete_companies.add(button_all, button_selectively)
    return keyboard_delete_companies
