# -*- coding: utf-8 -*-
"""
Модуль взаимодествия с клавиатурой выбора теории.
"""
from telebot import types

def get_keyboard() -> types.InlineKeyboardMarkup:
    """
    Цель: Инициализация клавиатуры теории.
    Возвращает: Клавиатуру выбора теории.
    """ 
    keyboard_theory = types.InlineKeyboardMarkup(row_width=1)
    button_investment = types.InlineKeyboardButton(text="Инвестирование",
                                                callback_data="Инвестирование")
    button_trading = types.InlineKeyboardButton(text="Трейдинг",
                                                callback_data="Трейдинг")
    keyboard_theory.add(button_investment, button_trading)
    return keyboard_theory
