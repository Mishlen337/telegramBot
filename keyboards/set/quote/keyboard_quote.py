# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой выбора котировки.
"""
from telebot import types

def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры котировки.
    Возвращает: Клавиатуру выбора котировки.
    """
    keyboard_quote = types.InlineKeyboardMarkup(row_width=1)
    button_ruble = types.InlineKeyboardButton(text="В рублях",
                                            callback_data="Рубль")
    button_currency = types.InlineKeyboardButton(text="В исходной валюте",
                                                callback_data="Валюта")
    keyboard_quote.add(button_ruble, button_currency)
    return keyboard_quote
